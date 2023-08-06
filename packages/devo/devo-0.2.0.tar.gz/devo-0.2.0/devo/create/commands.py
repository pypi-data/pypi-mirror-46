from pathlib import Path

import click
from cookiecutter.main import cookiecutter

PROJECT_TEMPLATE_DIR = Path(__file__).parent.parent / 'templates/project'


def cb(*args, **kwargs):
    print(args)
    print(kwargs)


@click.command()
@click.argument('project_name')
@click.option('--registry-url', prompt=True, default='')
@click.option('--registry-user', prompt=True)
@click.option('--registry-password', prompt=True)
@click.option('--registry-namespace', prompt=True)
def create(project_name, registry_url, registry_user, registry_password, registry_namespace):
    if (Path.cwd() / project_name).exists():
        click.secho(f'Directory {project_name} exists already')
        raise click.Abort()
    cookiecutter(str(PROJECT_TEMPLATE_DIR), no_input=True, extra_context={
        'project_name': project_name,
        'registry_url': registry_url,
        'registry_user': registry_user,
        'registry_password': registry_password,
        'registry_namespace': registry_namespace
    })


