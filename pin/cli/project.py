import os
from pathlib import Path

import click

from .utils import splash_screen
from .utils import copytree
from .utils import load_template
from .utils import PROJECT_DIR


@click.command("create", help="Create a new project.")
@click.argument("name")
@click.option("--version", "-v", prompt="Project version", help="Version of the project.")
def create(name, version):
    """
    Create a new project.
        $ pin create PROJECT_NAME
    will generate a new project folder containing boilerplate of the new project.
    To then add a new script, just type
        $ pin script add SCRIPT_NAME
    """
    click.echo(splash_screen())
    lib_name = name.replace("-", "_").replace(" ", "_")

    base_path = Path(os.getcwd()) / lib_name
    os.mkdir(base_path)

    # create config
    os.mkdir(base_path / "config")
    os.mkdir(base_path / "config/default")
    copytree(PROJECT_DIR / "templates/config/default", base_path / "config/default")

    # create build folder
    os.mkdir(base_path / "build")

    # create setup file
    setup_content = load_template("setup.tpl", NAME=name, VERSION=version)

    with open(base_path / "setup.py", "w") as setup_file:
        setup_file.write(setup_content)
    os.mkdir(base_path / name)

    # create base lib
    os.mkdir(base_path / lib_name)
    os.mkdir(base_path / lib_name / "utils")
    constants_content = load_template("constants.py")

    with open(base_path / name / "utils/constants.py", "w") as constants_file:
        constants_file.write(constants_content)

    click.echo(f"Project successfully created in {base_path}")