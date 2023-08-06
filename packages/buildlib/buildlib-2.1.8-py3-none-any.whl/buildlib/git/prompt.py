import prmt
from headlines import h3

from ..git import _lib as git
from ..git import _lib_cmd as git_cmd


def commit_msg(
    fmt=None,
    open_editor: bool = True,
) -> str:

    return prmt.string(
        question='Enter COMMIT message:\n',
        fmt=fmt,
        blacklist=[''],
        open_editor=open_editor,
    )


def branch(
    default=None,
    fmt=None,
) -> str:

    default = git_cmd.get_default_branch().val

    return prmt.string(
        question='Enter BRANCH name:\n',
        default=default,
        fmt=fmt,
    )


def confirm_status(
    default: str = 'y',
    fmt=None,
) -> bool:

    print(h3('Git Status'))
    git_cmd.status()

    return prmt.confirm(
        question='GIT STATUS ok?\n',
        default=default,
        fmt=fmt,
    )


def confirm_diff(
    default: str = 'y',
    fmt=None,
) -> bool:

    print(h3('Git Diff'))
    git_cmd.diff()

    return prmt.confirm(
        question='GIT DIFF ok?\n',
        default=default,
        fmt=fmt,
    )


def should_run_git(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='Run ANY GIT COMMANDS?\n',
        default=default,
        fmt=fmt,
    )


def should_add_all(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='Run GIT ADD ALL ("git add --all")?\n',
        default=default,
        fmt=fmt,
    )


def should_commit(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='Run GIT COMMIT?\n',
        default=default,
        fmt=fmt,
    )


def should_tag(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='Run GIT TAG?\n',
        default=default,
        fmt=fmt,
    )


def should_push(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='GIT PUSH to GITHUB?\n',
        default=default,
        fmt=fmt,
    )
