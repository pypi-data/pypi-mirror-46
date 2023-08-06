from pathlib import Path

from devo.utils import render_template_env_to_target


def generate_gitlab_ci(ctx, force):
    render_template_env_to_target('ci', Path.cwd(), ctx, force)


def generate_skaffold(ctx, force):
    render_template_env_to_target('skaffold', Path.cwd(), ctx, force)


def generate_k8s(ctx, force):
    render_template_env_to_target('k8s', Path.cwd() / 'k8s', ctx, force)

    for overlay in ctx['overlays']:
        overlay_dir = 'overlays/' + overlay
        overlay_target = Path.cwd() / 'k8s/overlays/' / overlay
        render_template_env_to_target(overlay_dir, overlay_target, ctx, force)


def generate_project(ctx, force):
    project_target = Path.cwd() / ctx['project_name']
    render_template_env_to_target('project', project_target, ctx, force)
