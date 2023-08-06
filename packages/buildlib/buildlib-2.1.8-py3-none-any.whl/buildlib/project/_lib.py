import subprocess as sp
from cmdi import CmdResult, command, set_result, strip_args
from buildlib.semver import prompt as semver_prompt
from buildlib import yaml


def bump_version(
    semver_num: str = None,
    config_file: str = 'Project',
) -> str:

    cfg: dict = yaml.loadfile(config_file)

    if not semver_num:
        semver_num = semver_prompt.semver_num_by_choice(cfg['version'])

    cfg.update({'version': semver_num})

    yaml.savefile(cfg, config_file)

    return semver_num
