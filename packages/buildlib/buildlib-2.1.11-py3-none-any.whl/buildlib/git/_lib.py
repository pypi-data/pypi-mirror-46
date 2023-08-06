import subprocess as sp
from typing import Optional, Union
from cmdi import command, CmdResult, set_result, strip_args


def add_all() -> None:

    sp.run(
        ['git', 'add', '--all'],
        check=True,
    )


def commit(msg: str) -> None:

    sp.run(
        ['git', 'commit', '-m', msg],
        check=True,
    )


def tag(
    version: str,
    branch: str,
) -> None:

    sp.run(
        ['git', 'tag', version, branch],
        check=True,
    )


def push(branch: str) -> None:

    sp.run(
        ['git', 'push', 'origin', branch, '--tags'],
        check=True,
    )


def get_default_branch() -> Union[str, None]:

    branch: Union[str, None] = None

    p1 = sp.run(
        ['git', 'show-branch', '--list'],
        stdout=sp.PIPE,
        check=True,
    )

    if p1.stdout.decode().find('No revs') == -1 and p1.returncode == 0:
        p2 = sp.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            stdout=sp.PIPE,
            check=True,
        )

        branch = p2.stdout.decode().replace('\n', '')

    return branch


def status() -> None:

    sp.run(
        ['git', 'status'],
        check=True,
    )


def diff() -> None:

    sp.run(
        ['git', 'diff'],
        check=True,
    )
