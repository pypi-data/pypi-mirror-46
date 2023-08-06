import click

from .kube.commands import kube


@click.group()
def cli():
    pass


cli.add_command(kube)

if __name__ == '__main__':
    cli()
