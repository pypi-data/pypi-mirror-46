import click

from .create.commands import create
from .build.commands import build
from .dev.commands import dev
from .deploy.commands import deploy
from .delete.commands import delete
from .kube.commands import kube


@click.group()
def cli():
    pass


cli.add_command(create)
cli.add_command(build)
cli.add_command(dev)
cli.add_command(deploy)
cli.add_command(delete)
cli.add_command(kube)

if __name__ == '__main__':
    cli()
