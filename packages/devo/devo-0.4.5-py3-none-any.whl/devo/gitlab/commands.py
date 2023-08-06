import click
import gitlab as glapi

from devo.config import read_config, persist_config, read_creds, persist_creds
from .utils import sync_variables_to_gitlab


@click.group()
def gitlab():
    pass


@gitlab.command()
@click.option('--url', prompt=True)
@click.option('--group', prompt=True)
@click.option('--project', prompt=True)
@click.option('--user', prompt=True)
@click.option('--password', prompt=True)
@click.option('--kube-url', prompt=True)
@click.option('--kube-user', prompt=True)
@click.option('--kube-token', prompt=True)
@click.option('--create', prompt=True, is_flag=True, default=False)
@click.option('--sync', prompt=True, is_flag=True, default=False)
def activate(url, group, project, user, password, kube_url, kube_user, kube_token, create, sync):
    gl = glapi.Gitlab(url, password)

    try:
        gl_group = gl.groups.list(search=group)[0]
    except IndexError:
        click.secho(f'Could not find group {group} on {url}', fg='red')
        gl_group = None
        if not create:
            raise click.Abort()
    except glapi.GitlabError as e:
        click.secho(f'GitLab error: {e}')
        raise click.Abort()

    if gl_group is None and create:
        try:
            click.echo(f'Creating group {group}')
            gl_group = gl.groups.create({'name': group, 'path': group})
        except glapi.GitlabError as e:
            click.secho(f'GitLab error: {e}', fg='red')
            raise click.Abort()

    try:
        gl_project = gl_group.projects.list(search=project)[0]
    except IndexError:
        click.secho(f'Could not find project {project} in group {group}', fg='red')
        gl_project = None
        if not create:
            raise click.Abort()
    except glapi.GitlabError as e:
        click.secho(f'GitLab error: {e}')
        raise click.Abort()

    if gl_project is None and create:
        try:
            click.echo(f'Creating project {project}')
            gl_project = gl.projects.create({'name': project, 'namespace_id': gl_group.id})
        except glapi.GitlabError as e:
            click.secho(f'GitLab error: {e}', fg='red')
            raise click.Abort()

    config = read_config()
    config['gitlab']['enabled'] = True
    config['gitlab']['url'] = url
    config['gitlab']['group'] = group
    config['gitlab']['project'] = project
    config['gitlab']['project_id'] = gl_project.id
    config['gitlab']['namespace_id'] = gl_group.id
    config['gitlab']['kube_url'] = kube_url
    config['gitlab']['kube_user'] = kube_user
    config['gitlab']['kube_token'] = kube_token
    persist_config(config)

    creds = read_creds()
    creds['gitlab_user'] = user
    creds['gitlab_password'] = password
    creds['kube_url'] = kube_url
    creds['kube_user'] = kube_user
    creds['kube_token'] = kube_token
    persist_creds(creds)

    if sync:
        sync_variables_to_gitlab()


@gitlab.command()
def sync_variables():
    sync_variables_to_gitlab()
