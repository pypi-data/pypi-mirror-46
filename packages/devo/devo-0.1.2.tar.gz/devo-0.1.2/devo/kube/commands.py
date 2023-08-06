import click

from .utils import execute_tests, deploy_test_env, cleanup_test_env


@click.group()
def kube():
    pass


@kube.command()
@click.option('--namespace')
@click.option('--registry-url')
@click.option('--registry-user')
@click.option('--registry-password')
def before_test(namespace, registry_url, registry_user, registry_password):
    deploy_test_env(namespace, registry_url, registry_user, registry_password)


@kube.command()
@click.option('--namespace')
def test(namespace):
    execute_tests(namespace)


@kube.command()
@click.option('--namespace')
def after_test(namespace):
    cleanup_test_env(namespace)
