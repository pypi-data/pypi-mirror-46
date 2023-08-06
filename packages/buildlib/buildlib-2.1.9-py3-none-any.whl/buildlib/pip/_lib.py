from cmdi import CmdResult, command, set_result, strip_args
import subprocess as sp


def freeze(
    sudo: bool = False,
    pip_bin: str = 'pip',
    requirements_file: str = 'requirements.txt',
    options: list = None,
) -> None:
    """
    Freeze current dependencies into 'requirements.txt'.
    """

    options = options or []
    sudo_cmd = 'sudo ' if sudo else ''

    if requirements_file:
        cmd = [
            sudo_cmd + pip_bin + ' freeze > ' + requirements_file + ' ' +
            ' '.join(options)
        ]

    else:
        cmd = [sudo_cmd + pip_bin + ' freeze ' + ' '.join(options)]

    sp.run(
        cmd,
        shell=True,
        check=True,
    )


def install(
    package: str,
    sudo: bool = False,
    pip_bin: str = 'pip',
    options: list = None,
) -> None:
    """
    Run 'pip install'.
    You can define 'pip_bin' to select a pip binary for a certain environment.
    """
    options = options or []
    sudo_cmd = 'sudo ' if sudo else ''

    cmd = [
        sudo_cmd + pip_bin + ' install ' + package + ' ' + ' '.join(options)
    ]

    sp.run(
        cmd,
        shell=True,
        check=True,
    )


def install_requirements(
    sudo: bool = False,
    pip_bin: str = 'pip',
    requirements_file: str = '',
    options: list = None,
) -> None:
    """
    Install what is listed in 'requirements.txt'.
    """
    options = options or []
    sudo_cmd = 'sudo ' if sudo else ''

    cmd = [
        sudo_cmd + pip_bin + ' install -r ' + requirements_file + ' ' +
        ' '.join(options)
    ]

    sp.run(
        cmd,
        shell=True,
        check=True,
    )


def uninstall(
    package: str,
    sudo: bool = False,
    pip_bin: str = 'pip',
    options: list = None,
) -> None:
    """
    Run 'pip uninstall'.
    You can define 'pip_bin' to select a pip binary for a certain environment.
    """
    options = options or []
    sudo_cmd = 'sudo ' if sudo else ''

    cmd = [
        sudo_cmd + pip_bin + ' uninstall ' + package + ' ' + ' '.join(options)
    ]

    sp.run(
        cmd,
        shell=True,
        check=True,
    )
