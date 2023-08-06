import yaml as pyyaml
import oyaml as yaml
import sys
from typing import Any


def loadfile(file: str, safe=True) -> dict:
    """
    Load yaml file.
    """
    if safe:
        with open(file, 'r') as f:
            return yaml.safe_load(f.read())
    else:
        with open(file, 'r') as f:
            pyyaml.warnings({'YAMLLoadWarning': False})
            return yaml.load(f.read())


def savefile(data: Any, file: str, safe=True, **kwargs) -> None:
    """
    Save data to yaml file.
    """
    if safe:
        with open(file, 'w') as f:
            yaml.safe_dump(data=data, stream=f, **kwargs)
    else:
        with open(file, 'w') as f:
            yaml.dump(data=data, stream=f, **kwargs)


def pprint_yaml(data: Any) -> None:

    lines: list = yaml.dump(
        data,
        indent=4,
        block_seq_indent=4,
    ).splitlines(True)

    print(''.join([line for line in lines]))
