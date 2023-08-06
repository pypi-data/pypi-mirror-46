import os
import fnmatch
import configparser
import collections


Config = collections.namedtuple('Config', ['ignores', ])

CONFIG_NAME = '.crlintrc'


def load_config(workdir):
    if not os.path.exists(os.path.join(workdir, CONFIG_NAME)):
        raise FileNotFoundError(
            'Cannot found {config} config'.format(config=CONFIG_NAME)
        )

    config = configparser.ConfigParser()
    config.read(os.path.join(workdir, CONFIG_NAME))

    config_ignore_patterns = [
        pattern.strip()
        for pattern in config.get('ignore', 'patterns').split(',')
    ]

    return Config(ignores=config_ignore_patterns)


def walk_files_recursively(root_path):
    for root, _, files in os.walk(root_path):
        for file in files:
            yield os.path.join(root, file)


def is_ignore_file(file_path, ignore_patterns):
    return any(
        fnmatch.fnmatch(file_path, ignore_pattern)
        for ignore_pattern in ignore_patterns
    )
