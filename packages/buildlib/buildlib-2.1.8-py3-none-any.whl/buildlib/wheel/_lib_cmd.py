from typing import Optional
from cmdi import CmdResult, command, set_result, strip_args

from ..wheel import _lib


@command
def push_to_gemfury(
    wheel_file: str,
    **cmdargs,
) -> CmdResult:
    _lib.push_to_gemfury(**strip_args(locals()))
    return set_result()


@command
def push(
    repository='pypi',
    clean_dir: bool = False,
    **cmdargs,
) -> CmdResult:
    _lib.push(**strip_args(locals()))
    return set_result()


@command
def build(
    clean_dir: bool = False,
    **cmdargs,
) -> CmdResult:
    _lib.build(**strip_args(locals()))
    return set_result()
