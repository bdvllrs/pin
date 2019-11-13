import os
from pathlib import Path

import click

from pin.cli.utils import find_root_folder
from pin.cli.utils import load_template
from pin.cli.utils import PROJECT_DIR


@click.group("script", help="Manage scripts.")
def script_group():
    """
    Base for the script group.
        $ pin script --help
    to list all the available commands.
    """
    pass


@script_group.command("add", help="Add a new script.")
@click.argument("script_name")
@click.option("--template", "-t", default="default", help="Template file to use.")
def add_script(script_name, template):
    """
    Add a new script in the scripts folder according to the given template (defaults to the default template).
    """
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
    """
    List available templates
    """
    template_path = PROJECT_DIR / "templates/scripts"
    templates = os.listdir(template_path)
    click.echo("- " + "\n- ".join(templates))