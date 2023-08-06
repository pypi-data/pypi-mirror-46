import click

from devo.config import read_config, persist_config, config_to_context
from devo.generate.utils import generate_overlays


@click.group()
def overlay():
    pass


@overlay.command()
def database():
    config = read_config()
    if 'database' not in config['overlays']:
        config['overlays'].append('database')
    else:
        config['overlays'].remove('database')
    persist_config(config)

    generate_overlays(config_to_context(), True)


