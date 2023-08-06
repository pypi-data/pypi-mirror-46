import os
from pathlib import Path

import click

from devo.generate.utils import generate_project, generate_gitlab_ci, generate_k8s, generate_skaffold
from devo.config import config_to_context

from .utils import git_init


@click.command()
@click.argument('project_name')
@click.option('--registry-image', prompt=True)
@click.option('--registry-url', prompt=True, default='')
@click.option('--registry-user', prompt=True)
@click.option('--registry-password', prompt=True)
@click.option('--force', is_flag=True, default=False)
def create(project_name, registry_image, registry_url, registry_user, registry_password, force):
    if (Path.cwd() / project_name).exists() and not force:
        click.secho(f'Directory {project_name} exists already')
        raise click.Abort()

    ctx = {
        'project_name': project_name,
        'registry_image': registry_image,
        'registry_url': registry_url,
        'registry_user': registry_user,
        'registry_password': registry_password,
    }
    click.echo(f'Generating project folder {project_name}')
    generate_project(ctx, force)

    os.chdir(project_name)
    ctx = config_to_context()

    click.echo('Generating .gitlab-ci.yml')
    generate_gitlab_ci(ctx, force)

    click.echo('Generating k8s templates')
    generate_k8s(ctx, force)

    click.echo('Generating skaffold.yaml')
    generate_skaffold(ctx, force)

    click.echo('Setting up Git')
    git_init()
