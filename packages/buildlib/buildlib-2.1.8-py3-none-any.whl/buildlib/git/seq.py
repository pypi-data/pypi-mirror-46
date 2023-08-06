from typing import Optional, List, Union
from cmdi import CmdResult

from ..git import _lib as git
from ..git import _lib_cmd as git_cmd
from ..git import prompt


class GitSeqSettings:
    version: Optional[str] = None
    new_release: bool = True
    should_run_any: bool = True
    should_add_all: Optional[bool] = True
    should_commit: bool = True
    commit_msg: Optional[str] = 'No comment message.'
    should_tag: Optional[bool] = True
    should_push: Optional[bool] = True
    branch: str = 'master'


def get_settings_from_user(
    version: str,
    new_release: bool,
    check_status: bool = True,
    check_diff: bool = True,
    should_add_all: Optional[bool] = None,
    should_tag: Optional[bool] = None,
    should_push: Optional[bool] = None,
    commit_msg: Optional[str] = None,
) -> GitSeqSettings:

    s = GitSeqSettings()

    s.version = version
    s.new_release = new_release
    s.commit_msg = commit_msg
    s.should_add_all = should_add_all
    s.should_tag = should_tag
    s.should_push = should_push

    # Ask user to check status.
    if check_status and not prompt.confirm_status('y'):
        s.should_run_any = False
        return s

    # Ask user to check diff.
    if check_diff and not prompt.confirm_diff('y'):
        s.should_run_any = False
        return s

    # Ask user to run 'git add -A.
    if s.should_add_all is None:
        s.should_add_all = prompt.should_add_all(default='y')

    # Ask user to run commit.
    if not commit_msg:
        s.should_commit = prompt.should_commit(default='y')

    # Get commit msg from user.
    if s.should_commit and not commit_msg:
        s.commit_msg = prompt.commit_msg()

    # Ask user to run 'tag'.
    if s.should_tag is None:
        s.should_tag = prompt.should_tag(
            default='y' if s.new_release is True else 'n'
        )

    # Ask user to push.
    if s.should_push is None:
        s.should_push = prompt.should_push(default='y')

    # Ask user for branch.
    if any([s.should_tag, s.should_push]):
        s.branch = prompt.branch()

    return s


def bump_sequence(s: GitSeqSettings) -> List[CmdResult]:
    """"""
    results: List[CmdResult] = []

    # If any git commands should be run.
    if not s.should_run_any:
        return results

    # Run 'add -A'
    if s.should_add_all:
        results.append(git_cmd.add_all())

    # Run 'commit -m'
    if s.should_commit:
        results.append(git_cmd.commit(s.commit_msg))

    # Run 'tag'
    if s.should_tag:
        results.append(git_cmd.tag(s.version, s.branch))

    # Run 'push'
    if s.should_push:
        results.append(git_cmd.push(s.branch))

    return results


def bump_git(
    version: str,
    new_release: bool = True,
    check_status: bool = True,
    check_diff: bool = True,
    should_add_all: Optional[bool] = None,
    should_tag: Optional[bool] = None,
    should_push: Optional[bool] = None,
    commit_msg: Optional[str] = None,
):
    s = get_settings_from_user(
        version,
        new_release=new_release,
        check_status=check_status,
        check_diff=check_diff,
        should_add_all=should_add_all,
        should_tag=should_tag,
        should_push=should_push,
        commit_msg=commit_msg,
    )
    return bump_sequence(s)
