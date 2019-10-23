import os
import click
from pathlib import Path

from pin.utils import load_template, find_root_folder


def splash_screen():
    return """ _______  _____  ____  _____  
|_   __ \|_   _||_   \|_   _| 
  | |__) | | |    |   \ | |   
  |  ___/  | |    | |\ \| |   
 _| |_    _| |_  _| |_\   |_  
|_____|  |_____||_____|\____| 

Project INitializer.
"""


@click.group()
def cli():
    click.echo(splash_screen())


@cli.command("create", help="Create a new project.")
@click.argument("name")
@click.option("--version", "-v", prompt="Project version", help="Version of the project.")
def create(name, version):
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


@cli.group("add", help="Add new resources (scripts).")
def add_group():
    pass


@add_group.command("script", help="Add a new script.")
@click.argument("script_name")
@click.option("--template", "-p", default="script.tpl", help="Template file to use.")
def add_script(script_name, template):
    base_path = find_root_folder(Path(os.getcwd()))
    if not base_path:
        raise click.ClickException("There are no scripts folder.")
    project_name = str(base_path).split('/')[-1]

    script_content = load_template(template,
                                   PROJECT_NAME=project_name,
                                   SCRIPT_NAME=script_name)

    if (base_path / "scripts" / (script_name + ".py")).exists():
        raise click.ClickException(f"The script `{script_name}` already exists.")
    with open(base_path / "scripts" / (script_name + ".py"), 'w') as script_file:
        script_file.write(script_content)
    click.echo(f"Script {script_name} successfully created.")


if __name__ == "__main__":
    cli()
