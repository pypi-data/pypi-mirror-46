import subprocess as sp
import shutil
import os
import re


def inject_interface_into_readme(
    interface_file: str,
    readme_file: str = 'README.md',
) -> None:
    """
    Add content of help.txt into README.md
    Content of help.txt will be placed into the first code block (```) of README.md.
    If no code block is found, a new one will be added to the beginning of README.md.
    """
    readme_str: str = open(readme_file, 'r').read()
    interface_str = open(interface_file, 'r').read()

    help_str: str = f'```\n{interface_str}\n```'

    start: int = readme_str.find('```') + 3
    end: int = readme_str.find('```', start)

    if '```' in readme_str:
        mod_str: str = readme_str[0:start - 3] + help_str + readme_str[end +
                                                                       3:]
    else:
        mod_str = help_str + readme_str

    with open('README.md', 'w') as modified_readme:
        modified_readme.write(mod_str)


def build_read_the_docs(clean_dir: bool = False) -> None:
    """"""

    build_dir = f'{os.getcwd()}/docs/build'

    if clean_dir and os.path.isdir(build_dir):
        shutil.rmtree(build_dir)

    sp.run(
        ['make', 'html'],
        cwd='{}/docs'.format(os.getcwd()),
        check=True,
    )


def create_py_venv(
    py_bin: str,
    venv_dir: str,
) -> None:
    """
    NOTE: Consider useing pipenv.

    @interpreter: must be the exact interpreter name. E.g. 'python3.5'
    """
    sp.run(
        [py_bin, '-m', 'venv', venv_dir],
        check=True,
    )


def bump_py_module_version(file: str, new_version: str) -> None:
    """
    Search a file for a python module version definition:
    __version__ = 'xxx'
    and update the version string.
    """
    data = ''

    with open(file) as f:
        data = f.read()
        data = re.sub(
            pattern=r'__version__ = [\'|"].*[\'|"][ \t]*\n',
            repl=f"__version__ = '{new_version}'\n",
            string=data,
        )

    with open(file, 'r+') as f:
        f.write(data)
