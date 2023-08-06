import subprocess

import click

from devo.utils import render_k8s_yaml


@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.argument('skaffold_args', nargs=-1, type=click.UNPROCESSED)
def build(skaffold_args):
    render_k8s_yaml()
    command = ['skaffold', 'build', '-f', '.devo/k8s/skaffold.yaml'] + list(skaffold_args)
    subprocess.call(command)
