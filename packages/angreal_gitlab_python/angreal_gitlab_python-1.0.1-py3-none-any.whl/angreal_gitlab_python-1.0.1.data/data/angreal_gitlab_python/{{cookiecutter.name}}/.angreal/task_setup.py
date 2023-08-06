import os


import angreal
from angreal.integrations.virtual_env import VirtualEnv,venv_required

import click


here = os.path.dirname(__file__)
requirements = os.path.join(here,'..','requirements','requirements.txt')
requirements_dev = os.path.join(here,'..','requirements','dev.txt')


@angreal.command()
@angreal.option('--no_dev', is_flag=True, help='Do not setup a dev environment.')
@venv_required('{{cookiecutter.name}}')
def angreal_cmd(no_dev):
    """
    update/create the {{cookiecutter.name}} environment.
    """
    #create our virtual environment and activate it for the rest of this run.
    reqs = requirements_dev
    if no_dev:
        reqs = requirements

    venv = VirtualEnv(name='{{cookiecutter.name}}', python='python3',requirements=reqs)
    angreal.echo(click.style('Virtual environment {} updated.'.format('{{cookiecutter.name}}'), fg='green'))
    return
