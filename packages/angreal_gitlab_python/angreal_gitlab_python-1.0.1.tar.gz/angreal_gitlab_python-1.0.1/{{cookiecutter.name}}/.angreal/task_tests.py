import angreal
import os
import subprocess
import webbrowser
from angreal.integrations.virtual_env import venv_required

here = os.path.realpath(os.path.dirname(__file__))
cwd = os.getcwd()


@angreal.command()
@angreal.option('--open', is_flag=True, help='generate an html report and open in a browser')
@venv_required('{{cookiecutter.name}}')
def angreal_cmd(open):
    """
    run package tests
    """
    os.chdir(os.path.join(here, '..'))

    if open:
        output_file = os.path.realpath(os.path.join(here,'..', 'htmlcov', 'index.html'))
        subprocess.run('pytest -vvv --cov={{cookiecutter.name}} --cov-report html',shell=True)
        webbrowser.open_new('file://{}'.format(output_file))
    else :
        subprocess.run('pytest -vvv --cov={{cookiecutter.name}}', shell=True)
    return
