import click

from .utils import generate_gitlab_ci, generate_skaffold, generate_k8s, generate_overlays

from devo.config import config_to_context


@click.group()
def generate():
    pass


@generate.command()
@click.option('--force', is_flag=True, default=False)
def gitlab_ci(force):
    ctx = config_to_context()
    generate_gitlab_ci(ctx, force)


@generate.command()
@click.option('--force', is_flag=True, default=False)
def skaffold(force):
    ctx = config_to_context()
    generate_skaffold(ctx, force)


@generate.command()
@click.option('--force', is_flag=True, default=False)
def k8s(force):
    ctx = config_to_context()
    generate_k8s(ctx, force)


@generate.command()
@click.option('--force', is_flag=True, default=False)
def overlays(force):
    ctx = config_to_context()
    generate_overlays(ctx, force)
