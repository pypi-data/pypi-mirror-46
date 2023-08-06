from collections import defaultdict
from pathlib import Path

from ruamel.yaml import YAML

CONFIG_DIRECTORY = Path.cwd() / '.devo'
CONFIG_FILE_PATH = CONFIG_DIRECTORY / 'config.yaml'

yaml = YAML()


def config_dict():
    return defaultdict(dict)


def read_config():
    data = config_dict()
    data.update(yaml.load(CONFIG_FILE_PATH))
    return data


