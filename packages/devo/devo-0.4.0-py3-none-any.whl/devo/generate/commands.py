import click

from .utils import generate_gitlab_ci, generate_skaffold, generate_k8s


@click.group()
def generate():
    pass


@generate.command()
@click.option('--force', is_flag=True, default=False)
def gitlab_ci(force):
    generate_gitlab_ci(force)


@generate.command()
@click.option('--force', is_flag=True, default=False)
def skaffold(force):
    generate_skaffold(force)


@generate.command()
@click.option('--force', is_flag=True, default=False)
def k8s(force):
    generate_k8s(force)
