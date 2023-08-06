import json
from typing import Optional
from cmdi import CmdResult, command, set_result, strip_args
import subprocess as sp


def bump_version(
    new_version: str,
    filepath: str = 'package.json',
    indent: Optional[int] = 4,
) -> None:

    with open(filepath, 'r') as f:
        data = json.load(f)

    data['version'] = new_version

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def publish() -> None:
    """"""
    sp.run(
        ['npm', 'publish'],
        check=True,
    )
