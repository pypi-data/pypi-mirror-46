"""
    {{ cookiecutter.name }}.cli
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    {{ cookiecutter.name}}'s command line interface

"""

import click


@click.group()
def main():
    """
    The main entry point for {{cookiecutter.name}}
    :return:
    """
    pass


@main.command()
def subcommand():
    """
    This is a sub command on the main entry point group
    :return:
    """
    pass