import json
from typing import Optional
from cmdi import CmdResult, command, set_result, strip_args
import subprocess as sp

from ..npm import _lib


@command
def bump_version(
    new_version: str,
    filepath: str = 'package.json',
    **cmdargs,
) -> CmdResult:
    _lib.bump_version(**strip_args(locals()))
    return set_result()


@command
def publish(**cmdargs) -> CmdResult:
    _lib.publish()
    return set_result()
