import os
from pathlib import Path
from shutil import rmtree

import click

from .utils import splash_screen
from .utils import copytree
from .utils import load_template
from .utils import PROJECT_DIR


@click.command("create", help="Create a new project.")
@click.argument("name")
@click.option("--version", "-v", default="0.0.1", help="Version of the project.")
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
    if base_path.exists():
        overwrite_project_confirm = click.confirm(f"Folder {lib_name} already exists. "
                                                  "Do you want to overwrite it?")
        if not overwrite_project_confirm:
            click.echo("Aborted.")
            return
        rmtree(base_path)
    os.mkdir(base_path)
    os.mkdir(base_path / "scripts")

    # create config
    os.mkdir(base_path / "config")
    copytree(PROJECT_DIR / "templates/config", base_path / "config")

    # create build folder
    os.mkdir(base_path / "build")

    # create setup file
    setup_content = load_template("setup.tpl", NAME=name, VERSION=version)
    with open(base_path / "setup.py", "w") as setup_file:
        setup_file.write(setup_content)

    # create base lib
    os.mkdir(base_path / lib_name)
    os.mkdir(base_path / lib_name / "utils")

    constants_content = load_template("constants.tpl")
    with open(base_path / name / "utils/constants.py", "w") as constants_file:
        constants_file.write(constants_content)

    git_ignore_content = load_template(".gitignore.tpl")
    with open(base_path / ".gitignore", "w") as gitignore_file:
        gitignore_file.write(git_ignore_content)

    click.echo(f"Project successfully created in {base_path}.")
