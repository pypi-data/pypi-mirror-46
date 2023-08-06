import os
import sys
import traceback
from typing import Dict, Iterable, Tuple, Union

ConfigValueType = Union[None, bool, int, float, str, bytes]


def _read_config_file(config_path: str) -> Dict[str, ConfigValueType]:
    config_path_from_env = os.getenv('CONFIG_PATH')
    if config_path_from_env is not None:
        print('Replace config path with environment variable.',
              file=sys.stderr)
        config_path = config_path_from_env

    try:
        with open(config_path, encoding='utf-8') as f:
            config_source = f.read()
    except FileNotFoundError:
        print('Cannot find config file at "%s".' % config_path,
              file=sys.stderr)
        sys.exit(1)

    try:
        config_module_variables: Dict[str, ConfigValueType] = dict()
        exec(config_source, config_module_variables)  # nosec
    except Exception:
        traceback.print_exc()
        print('Failed to evaluate config file.', file=sys.stderr)
        sys.exit(1)

    config: Dict[str, ConfigValueType] = dict()
    for k, v in config_module_variables.items():
        if not k.startswith('_') and k.isupper():
            config[k] = v

    return config


class ConfigProxy:
    def __init__(self, config_dict: Dict[str, ConfigValueType]):
        self._config_dict = config_dict

    def items(self) -> Iterable[Tuple[str, ConfigValueType]]:
        return self._config_dict.items()

    def get(self, key: str, d: ConfigValueType = None) -> ConfigValueType:
        return self._config_dict.get(key, d)

    def ensure(self, key: str) -> None:
        if key not in self._config_dict:
            raise KeyError('Configuration key "%s" is missing!' % key)

    def extract(self, *keys: str):
        keys_ordered, last_idx = list(self._config_dict.keys()), -1
        for key in keys:
            self.ensure(key)
            key_idx = keys_ordered.index(key)
            if key_idx < last_idx:
                raise KeyError(
                    'The key "%s" violates the order defined in config!' % key)
            elif key_idx == last_idx:
                raise KeyError('The key "%s" is duplicated!' % key)
            else:
                last_idx = key_idx

        return ConfigProxy({key: self._config_dict[key] for key in keys})

    def __getattr__(self, key: str) -> ConfigValueType:
        return self._config_dict[key]

    def __getitem__(self, key: str) -> ConfigValueType:
        return self._config_dict[key]


def load_config(config_path: str = 'configs/default.py') -> ConfigProxy:
    return ConfigProxy(_read_config_file(config_path))
