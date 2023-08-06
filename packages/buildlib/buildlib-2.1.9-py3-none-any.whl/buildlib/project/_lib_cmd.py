from cmdi import CmdResult, command, set_result, strip_args

from ..project import _lib


@command
def bump_version(
    semver_num: str = None,
    config_file: str = 'Project',
    **cmdargs,
) -> CmdResult:
    return set_result(_lib.bump_version(**strip_args(locals())))
