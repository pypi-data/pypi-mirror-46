import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from devo.config import read_config

K8S_TEMPLATE_DIR = Path(__file__).parent / 'templates/k8s'
K8S_TARGET_DIR = Path.cwd() / '.devo/k8s'


def render_k8s_yaml():
    config = read_config()
    env = Environment(loader=FileSystemLoader(str(K8S_TEMPLATE_DIR)))
    ctx = {'project_name': config['project_name'],
           'registry_image': config['registry']['image']}
    for template in env.list_templates():
        output = K8S_TARGET_DIR / template
        if not output.parent.exists():
            os.makedirs(output.parent)
        env.get_template(template).stream(**ctx).dump(str(output))
