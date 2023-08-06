from cmdi import CmdResult, command, set_result, strip_args

from ..pip import _lib


@command
def freeze(
    sudo: bool = False,
    pip_bin: str = 'pip',
    requirements_file: str = 'requirements.txt',
    options: list = None,
    **cmdargs,
) -> CmdResult:
    _lib.freeze(**strip_args(locals()))
    return set_result()


@command
def install(
    package: str,
    sudo: bool = False,
    pip_bin: str = 'pip',
    options: list = None,
    **cmdargs,
) -> CmdResult:
    _lib.install(**strip_args(locals()))
    return set_result()


@command
def install_requirements(
    sudo: bool = False,
    pip_bin: str = 'pip',
    requirements_file: str = '',
    options: list = None,
    **cmdargs,
) -> CmdResult:
    _lib.install_requirements(**strip_args(locals()))
    return set_result()


@command
def uninstall(
    package: str,
    sudo: bool = False,
    pip_bin: str = 'pip',
    options: list = None,
    **cmdargs,
) -> CmdResult:
    _lib.uninstall(**strip_args(locals()))
    return set_result()
