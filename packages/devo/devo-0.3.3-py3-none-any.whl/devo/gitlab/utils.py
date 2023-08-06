import gitlab as glapi

from devo.config import read_config


def replace_variable(project, key, value):
    try:
        var = project.variables.get(key)
    except glapi.GitlabError as e:
        if e.response_code == 404:
            project.variables.create({'key': key, 'value': value})
            return
        else:
            raise e
    var.delete()
    project.variables.create({'key': key, 'value': value})


def sync_variables_to_gitlab():
    config = read_config()
    gl = glapi.Gitlab(config['gitlab']['url'], config['gitlab']['password'])

    project = gl.projects.get(config['gitlab']['project_id'])

    if not config['registry']['user'].startswith('$'):
        replace_variable(project, 'CI_REGISTRY_USER', config['registry']['user'])
    if not config['registry']['password'].startswith('$'):
        replace_variable(project, 'CI_REGISTRY_PASSWORD', config['registry']['password'])
    if config['registry']['url']:
        replace_variable(project, 'CI_REGISTRY', config['registry']['url'])

    replace_variable(project, 'KUBE_URL', config['gitlab']['kube_url'])
    replace_variable(project, 'KUBE_USER', config['gitlab']['kube_user'])
    replace_variable(project, 'KUBE_TOKEN', config['gitlab']['kube_token'])
