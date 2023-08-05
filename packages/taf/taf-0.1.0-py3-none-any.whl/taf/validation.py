import os

from taf.exceptions import InvalidBranch


def validate_branch(auth_repo, target_repos, branch_name):
  """
  Validates corresponding branches of the authentication repository
  and the target repositories. Assumes that:
  1. Commits of the target repositories' branches are merged into the default (master) branch
  2. Commits of the authentication repository are not merged into the default (master) branch
  directly - fresh timestamp and snapshot are generated.
  Checks if:
  1. For each target repository, a commit sha of each commit of the specified branch matches
  the commit sha stored in the target file corresponding to that repository.
  2. Versions of tuf metadata increase by one from one commit
  to the next commit of a branch in the authentication repository
  3. The last commit of the authentication repository's branch has capstone set (meaning
  that a capstone file is one of the targets specified in targets.json)
  4. If all commits of an authentication repository's branch have the same branch ID
  """

  check_capstone(auth_repo, branch_name)

  targets_and_commits = {target_repo: target_repo.
                         commits_on_branch_and_not_other(branch_name, 'master')
                         for target_repo in target_repos}
  auth_commits = auth_repo.commits_on_branch_and_not_other(branch_name, 'master')

  _check_lengths_of_branches(targets_and_commits, branch_name)

  targets_version = None
  branch_id = None
  targets_path = 'metadata/targets.json'

  # fill the shorter lists with None values, so that their sizes match the size
  # of authentication repository's commits list
  for commits in targets_and_commits.values():
    commits.extend([None] * (len(auth_commits) - len(commits)))

  for commit_index, auth_commit in enumerate(auth_commits):
    # load content of targets.json
    targets = auth_repo.get_json(auth_commit, targets_path)
    targets_version = _check_targets_version(targets, auth_commit, targets_version)
    branch_id = _check_branch_id(auth_repo, auth_commit, branch_id)

    for target, target_commits in targets_and_commits.items():
      target_commit = target_commits[commit_index]

      # targets' commits match the target commits specified in the authentication repository
      if target_commit is not None:
        _compare_commit_with_targets_metadata(auth_repo, auth_commit, target, target_commit)


def _check_lengths_of_branches(targets_and_commits, branch_name):
  """
  Checks if branches of the given name have the same number
  of commits in each of the provided repositories.
  """

  lengths = set(len(commits) for commits in targets_and_commits.values())
  if len(lengths) > 1:
    msg = f'Branches {branch_name} of target repositories do not have the same number of commits'
    for target, commits in targets_and_commits.items():
      msg += f'\n{target.target_path} has {len(commits)} commits.'
    raise InvalidBranch(msg)


def _check_branch_id(auth_repo, auth_commit, branch_id):

  new_branch_id = auth_repo.get_file(auth_commit, 'targets/branch')
  if branch_id is not None and new_branch_id != branch_id:
    raise InvalidBranch(f'Branch ID at revision {auth_commit} is not the same as the '
                        'version at the following revision')
  return new_branch_id


def _check_targets_version(targets, tuf_commit, current_version):
  """
  Checks version numbers specified in targets.json (compares it to the previous one)
  There are no other metadata files to check (when building a speculative branch, we do
  not generate snapshot and timestamp, just targets.json and we have no delegations)
  Return the read version number
  """
  new_version = targets['signed']['version']
  # substracting one because the commits are in the reverse order
  if current_version is not None and new_version != current_version - 1:
    raise InvalidBranch(f'Version of metadata file targets.json at revision '
                        f'{tuf_commit} is not equal to previous version incremented '
                        'by one!')
  return new_version


def check_capstone(auth_repo, branch):
  """
  Check if there is a capstone file (a target file called capstone) at the end of the specified branch.
  Assumes that the branch is checked out.
  """
  capstone_path = os.path.join(auth_repo.repo_path, 'targets', 'capstone')
  if not os.path.isfile(capstone_path):
    raise InvalidBranch(f'No capstone at the end of branch {branch}!!!')


def _compare_commit_with_targets_metadata(tuf_repo, tuf_commit, target_repo, target_repo_commit):
  """
  Check if commit sha of a repository's speculative branch commit matches the
  specified target value in targets.json.
  """
  targets_head_sha = tuf_repo.get_json(tuf_commit, f'targets/{target_repo.target_path}')['commit']
  if target_repo_commit != targets_head_sha:
    raise InvalidBranch(f'Commit {target_repo_commit} of repository {target_repo.name} does '
                        'not match the commit sha specified in targets.json!')
