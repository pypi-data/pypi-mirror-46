import subprocess
import shlex

GIT_INIT = """git init"""


def git_init():
    command = shlex.split(GIT_INIT)
    subprocess.call(command)

