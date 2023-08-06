import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from devo.config import read_config

K8S_TEMPLATES_DIR = Path(__file__).parent / 'templates/k8s'
K8S_TEMPLATES_TARGET_DIR = Path.cwd() / '.devo/k8s'

K8S_OVERLAY_DIR = Path(__file__).parent / 'templates/overlays'
K8S_OVERLAY_TARGET_DIR = Path.cwd() / '.devo/k8s/overlays'

TEMPLATE_DIR = Path(__file__).parent / 'templates'


def get_active_overlays(config):
    overlays = []

    try:
        if config['database']['enabled']:
            overlays.append('database')
    except KeyError:
        pass

    return overlays


def render_k8s_yaml():
    config = read_config()
    overlays = get_active_overlays(config)
    ctx = {'project_name': config['project_name'],
           'registry_image': config['registry']['image'],
           'overlays': overlays}

    render_templates_to_target(K8S_TEMPLATES_DIR, K8S_TEMPLATES_TARGET_DIR, ctx)

    for overlay in overlays:
        render_templates_to_target(K8S_OVERLAY_DIR / overlay, K8S_OVERLAY_TARGET_DIR / overlay, ctx)


def render_templates_to_target(template_dir, target_dir, ctx):
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    for template in env.list_templates():
        output = target_dir / template
        if not output.parent.exists():
            os.makedirs(output.parent)
        env.get_template(template).stream(**ctx).dump(str(output))


def get_template_env(env):
    module = str(TEMPLATE_DIR / env)
    return Environment(loader=FileSystemLoader(module))


def render_template_env_to_target(env, target_dir, ctx, force=False):
    env = get_template_env(env)
    for template in env.list_templates():
        output = target_dir / template
        if output.exists() and not force:
            continue
        if not output.parent.exists():
            os.makedirs(output.parent)
        env.get_template(template).stream(**ctx).dump(str(output))
