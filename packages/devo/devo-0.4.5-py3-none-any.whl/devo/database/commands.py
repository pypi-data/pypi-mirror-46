import click


from devo.config import read_config, persist_config, read_creds, persist_creds

from .utils import generate_password


@click.group()
def database():
    pass


@database.command()
def activate():
    config = read_config()
    creds = read_creds()
    config['database']['enabled'] = True
    creds['database']['password'] = generate_password(20)
    persist_config(config)
    persist_creds(creds)
