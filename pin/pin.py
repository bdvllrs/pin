import os
import click
from pathlib import Path
from subprocess import call

from .utils import copytree
from .utils import load_template, find_root_folder, find_and_get_sacred_conf
from .utils import PROJECT_DIR


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
    pass


@cli.command("create", help="Create a new project.")
@click.argument("name")
@click.option("--version", "-v", prompt="Project version", help="Version of the project.")
def create(name, version):
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


@cli.command("omniboard", help="Start omniboard using the project's sacred information.")
@click.option("--mongo", "-m", default="localhost:27017", type=str, help="MongoDB connexion information.")
@click.option("--database", "-d", default=None, help="MongoDB database to use.")
def omniboard(mongo, database):
    """
    Args:
        mongo:
        database:
    Returns:

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
        raise click.ClickException(f"Could not start omniboard. Is it installed?")


@cli.group("script", help="Manage scripts.")
def script_group():
    pass


@script_group.command("add", help="Add a new script.")
@click.argument("script_name")
@click.option("--template", "-t", default="default", help="Template file to use.")
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


@script_group.command("templates", help="List all templates.")
def list_templates():
    template_path = PROJECT_DIR / "templates/scripts"
    templates = os.listdir(template_path)
    click.echo("- " + "\n- ".join(templates))


if __name__ == "__main__":
    cli()
