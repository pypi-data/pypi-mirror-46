from collections import defaultdict
from pathlib import Path

from ruamel.yaml import YAML

CONFIG_FILE_PATH = Path.cwd() / 'devo.yaml'

HIDDEN_DIRECTORY = Path.cwd() / '.devo'
CREDENTIALS_FILE_PATH = HIDDEN_DIRECTORY / 'creds.yaml'

yaml = YAML()


def config_dict():
    return defaultdict(dict)


def read_yaml(filepath):
    data = config_dict()
    data.update(yaml.load(filepath))
    return data


def persist_yaml(filepath, data):
    config = yaml.load(filepath)
    config.update(data)
    yaml.dump(config, filepath)


def read_config():
    return read_yaml(CONFIG_FILE_PATH)


def persist_config(data):
    persist_yaml(CONFIG_FILE_PATH, data)


def read_creds():
    try:
        return read_yaml(CREDENTIALS_FILE_PATH)
    except FileNotFoundError:
        # Todo: read creds from env
        return []


def persist_creds(data):
    persist_yaml(CREDENTIALS_FILE_PATH, data)
