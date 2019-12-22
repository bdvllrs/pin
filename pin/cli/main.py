import click

from .config import config_group
from .project import create
from .sacred import omniboard
from .scripts import script_group


@click.group()
def cli():
    """
    Entry point of the CLI. You can execute other commands from here.
    For example:
    $ pin create
    to create a new project.

    Type a command with `--help` to get more information.
    """
    pass


cli.add_command(create)
cli.add_command(config_group)
cli.add_command(script_group)
cli.add_command(omniboard)

if __name__ == "__main__":
    cli()
