import click


@click.group()
def kube():
    pass


@kube.command()
def test():
    pass
