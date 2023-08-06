import click


from devo.config import read_config, persist_config

from .utils import generate_password


@click.group()
def database():
    pass


@database.command()
def activate():
    config = read_config()
    config['database']['enabled'] = True
    config['database']['password'] = generate_password(20)
    persist_config(config)
