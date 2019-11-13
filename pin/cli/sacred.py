import os
from pathlib import Path
from subprocess import call

import click

from pin.cli.utils import find_and_get_sacred_conf


@click.command("omniboard", help="Start omniboard using the project's sacred information.")
@click.option("--mongo", "-m", default="localhost:27017", type=str, help="MongoDB connexion information.")
@click.option("--database", "-d", default=None, help="MongoDB database to use.")
def omniboard(mongo, database):
    """
    Starts the omniboard command using the information filled in the sacred.yaml config.
    """
    sacred_config = find_and_get_sacred_conf(Path(os.getcwd()))
    if sacred_config is not None:
        database_name = sacred_config['sacred']['mongodb']['db_name']
    elif database is not None:
        database_name = database
    else:
        raise click.ClickException(f"The sacred config file could not be located. Is it really a pin project?")

    try:
        click.echo(f"> omniboard -m {mongo}:{database_name}")
        call(["omniboard", "-m", f"{mongo}:{database_name}"])
    except:
        raise click.ClickException(f"Could not start omniboard. Is it properly configured?")