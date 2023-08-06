import argparse
from pathlib import Path
from typing import Dict, Union

import yaml

__all__ = ['load']


def parse_config(config_path: Path, values: dict, recursive_mark: str, memo: dict):
    if isinstance(values, list):
        for item in values:
            parse_config(config_path, item, recursive_mark, memo)
    elif isinstance(values, dict):
        if recursive_mark in values.keys():
            refer_path = config_path.parent / Path(values.pop(recursive_mark))
            base_values = load(refer_path, recursive_mark=recursive_mark, memo=memo)
            base_values.update(values)
            values.update(base_values)
        for key, value in values.items():
            parse_config(config_path, value, recursive_mark, memo)


def load(config_path: Union[str, Path], recursive_mark: str = '$ref', memo: dict = None):
    config_path = Path(config_path)
    absolute_path = config_path.absolute()

    if memo is None:
        memo = dict()
    if absolute_path in memo:
        return memo[absolute_path]

    with open(str(config_path)) as f:
        dictionary: Dict[str, dict] = yaml.load(f, Loader=yaml.SafeLoader)

    parse_config(config_path=config_path, values=dictionary, recursive_mark=recursive_mark, memo=memo)

    memo[absolute_path] = dictionary
    return dictionary


def main():  # pragma: no cover
    arg_parser = argparse.ArgumentParser(description='Load YAML recursively')
    arg_parser.add_argument('yaml_path', type=str)
    arg_parser.add_argument('-m', '--mark', type=str, default='$ref')
    arguments = arg_parser.parse_args()

    result = load(config_path=arguments.yaml_path, recursive_mark=arguments.mark)
    print(yaml.dump(result))


if __name__ == '__main__':
    main()  # pragma: no cover
