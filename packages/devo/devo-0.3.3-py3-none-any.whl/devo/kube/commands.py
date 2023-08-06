import click

from .utils import execute_tests, deploy_test_env, cleanup_test_env, init_kubectl
from devo.utils import render_k8s_yaml


@click.group()
def kube():
    pass


@kube.command()
@click.option('--name')
@click.option('--url')
@click.option('--user')
@click.option('--token')
def init(name, url, user, token):
    init_kubectl(name, url, user, token)


@kube.command()
@click.argument('namespace')
@click.option('--registry-url')
@click.option('--registry-user')
@click.option('--registry-password')
def before_test(namespace, registry_url, registry_user, registry_password):
    deploy_test_env(namespace, registry_url, registry_user, registry_password)


@kube.command()
@click.argument('namespace')
def test(namespace):
    execute_tests(namespace)


@kube.command()
@click.argument('namespace')
def after_test(namespace):
    cleanup_test_env(namespace)


@kube.command()
def debug():
    render_k8s_yaml()
