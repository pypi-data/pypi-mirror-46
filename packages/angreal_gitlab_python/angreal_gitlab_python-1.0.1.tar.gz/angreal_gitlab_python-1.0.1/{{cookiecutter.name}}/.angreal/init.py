import sys
import stat
import os
import subprocess


import angreal
from angreal.replay import Replay
from angreal.integrations.virtual_env import VirtualEnv
from angreal.integrations.git import Git
from angreal.integrations.gl import GitLab

import click


here = os.path.dirname(__file__)

pypirc = os.path.expanduser(os.path.join('~','.pypirc'))
requirements = os.path.join(here,'..','requirements','dev.txt')
setup_py = os.path.join(here,'..','setup.py')

@angreal.command()
@angreal.option('--gitlab_token',envvar='GITLAB_TOKEN', help='gitlab token to use (default = $GITLAB_TOKEN)')
@angreal.option('--no_pypi', is_flag=True, help='do not setup a pypi registry')
@angreal.option('--no_gitlab', is_flag=True, help='no gitlab project created')
def init(gitlab_token, no_pypi, no_gitlab):
    """
    initialize a python project
    """

    #Get our replay
    replay = Replay()

    #create our virtual environment and activate it for the rest of this run.

    venv = VirtualEnv(name='{{cookiecutter.name}}', python='python3',requirements=requirements)
    angreal.echo(click.style('Virtual environment {} created'.format('{{cookiecutter.name}}'), fg='green'))

    if not no_pypi: #double negative, skipped if no_pypi == True
        #Get a pypirc setup if one doesn't exist.
        if not os.path.isfile(pypirc):
            rv = input('No pypirc file detected do you wish to continue upload ? y/[n]')
            if rv == 'y':
                pypi_un = input('What is your pypi user name ?')
                pypi_pw = input('What is your pypi password ?')
                with open(pypirc,'w') as f:
                    print('[server-login]', file = f)
                    print('username: {}'.format(pypi_un), file = f)
                    print('password: {}'.format(pypi_pw), file = f)
                os.chmod(pypirc, stat.S_IRUSR )

            # Register with a 0.0.0 upload
                rv = subprocess.run('python {} bdist_wheel upload'.format(setup_py),
                                    shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                if rv.returncode != 0:
                    angreal.echo(
                        click.style('No pypi registry reserved, probably due to a collision in namespaces.',
                                    fg='yellow'))
                    raise NameError(r.stderr, r.stdout)

                angreal.echo(click.style('{{cookiecutter.name}} version 0.0.0 reserved on pypi.', fg='green'))
            else :
                pass



    else :
        angreal.echo(click.style('No pypi registry reserved, use `python setup.py bdist_wheel upload` later if you wish.',fg='yellow'))


    if not no_gitlab:
        # Now go get our Gitlab project
        project = GitLab('https://gitlab.com',token=gitlab_token)


        # Get our namespace
        requested_namespace = replay.get('namespace')

        if requested_namespace != 'user':
            project.create_repository(replay.get('name'),name_space_id=requested_namespace)
            angreal.echo(click.style('{} created'.format(project.project.ssh_url_to_repo),fg='green'))
        else :
            project.create_project(replay.get('name'))
            angreal.echo(click.style('{} created'.format(project.project.ssh_url_to_repo), fg='green'))

        project.enable_gitlfs()
        project.enable_issues()
        project.enable_pipelines()

    #Initialize the git repo and push to the remote
    git = Git()
    git.init()
    git.add('.')
    if not no_gitlab:
        git.remote('add', 'origin', project.project.ssh_url_to_repo)
        git.commit('-m', 'Project initialized via angreal.')
        git.push('origin','master')

    angreal.echo(click.style('{{ cookiecutter.name }} successfully created !',fg='green'))
    return
