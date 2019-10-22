import os
import argparse
import shutil
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[0]

possible_commands = ["create", "add_script"]


def exit():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def get_arguments():
    parser = argparse.ArgumentParser(description="Generate a new project structure.")
    parser.add_argument("command", help=f"Command to use. Among {', '.join(possible_commands)}.")
    parser.add_argument("--name", "-n", default=None, help=f"Name to use.")
    parser.add_argument("--template", "-t", default="script.tpl", help=f"Script template file to use.")

    return parser.parse_args()


def error_if_empty(message):
    if len(message) == 0:
        return True
    return False


def fits_all_callbacks(callbacks, answer):
    if callbacks is None:
        return True
    for callback in callbacks:
        if callback(answer):
            return False
    return True


def get_prompt(message, default, error_callbacks=None):
    while "The answer is not correct":
        prompt_message = input(f"{message} [{default}]: ").strip()
        prompt_message = default if len(prompt_message) == 0 else prompt_message
        if fits_all_callbacks(error_callbacks, prompt_message):
            break
        else:
            print("Please give a valid value.")

    return prompt_message


def get_preferences():
    preferences = dict()
    preferences['name'] = get_prompt("Project name", "", [error_if_empty])
    preferences['lib_name'] = preferences['name'].replace("-", "_")
    preferences['version'] = get_prompt("Project version", "0.0.1")
    preferences['description'] = get_prompt("Project description", "")
    preferences['config'] = get_prompt("Configuration folder", "config")
    preferences['build'] = get_prompt("Build folder", "builds")
    preferences['script'] = get_prompt("Script folder", "scripts")

    return preferences


def build_config(base_path, preferences):
    os.mkdir(base_path / preferences['config'])
    os.mkdir(base_path / preferences['config'] / "default")
    copytree(PROJECT_DIR / "templates/config/default", base_path / preferences['config'] / "default")


def build_builds(base_path, preferences):
    os.mkdir(base_path / preferences['build'])


def build_setup(base_path, preferences):
    setup_content = load_template("setup.tpl", NAME=preferences['name'], VERSION=preferences['version'])

    with open(base_path / "setup.py", "w") as setup_file:
        setup_file.write(setup_content)
    os.mkdir(base_path / preferences['name'])


def build_base_lib(base_path, preferences):
    os.mkdir(base_path / preferences['lib_name'])
    os.mkdir(base_path / preferences['lib_name'] / "utils")
    constants_content = load_template("constants.py")

    with open(base_path / preferences['name'] / "utils/constants.py", "w") as constants_file:
        constants_file.write(constants_content)


def splash_screen():
    print(""" _______  _____  ____  _____  
|_   __ \|_   _||_   \|_   _| 
  | |__) | | |    |   \ | |   
  |  ___/  | |    | |\ \| |   
 _| |_    _| |_  _| |_\   |_  
|_____|  |_____||_____|\____| \n""")
    print("Project Initializer.")


def script_create_project(args):
    splash_screen()

    print("Answer some question to personalize your project...")

    preferences = get_preferences()

    base_path = Path(os.getcwd()) / preferences['lib_name']

    os.mkdir(base_path)

    build_config(base_path, preferences)
    build_builds(base_path, preferences)
    build_setup(base_path, preferences)
    build_base_lib(base_path, preferences)

    print(f"Project successfully created in {base_path}")


def load_template(template_name, **vars):
    base_path = Path(os.getcwd())
    template_file_path = PROJECT_DIR / "templates" / template_name
    if (base_path / template_name).exists():
        template_file_path = base_path / template_name
    elif Path(template_name).exists():
        template_file_path = Path(template_name)
    elif not template_file_path.exists():
        print("Template file not found.")
        exit()

    with open(template_file_path, "r") as template_file:
        template_content = template_file.read()
    for var, value in vars.items():
        template_content = template_content.replace(f"%{var}%", value)
    return template_content


def script_add_script(args):
    """
    Add a new script.
    """
    base_path = Path(os.getcwd())
    project_name = str(base_path).split('/')[-1]
    project_name = get_prompt("Project name", project_name)
    script_name = get_prompt("Script name", "main")
    script_folder = get_prompt("Script folder", "scripts")

    script_content = load_template(args.template,
                                   PROJECT_NAME=project_name,
                                   SCRIPT_NAME=script_name)

    with open(base_path / script_folder / (script_name + ".py"), 'w') as script_file:
        script_file.write(script_content)
    print(f"Script {script_name} successfully created.")


def execute_script(args):
    """
    Start the correct script.
    """
    if args.command == "create":
        script_create_project(args)
    elif args.command == "add_script":
        script_add_script(args)
    else:
        print(f"Command incorrect. Choose among {', '.join(possible_commands)}.")


def clean_script(args):
    """
    Called when script is cancelled.
    """
    pass


if __name__ == "__main__":
    args = get_arguments()

    try:
        execute_script(args)
    except KeyboardInterrupt:
        clean_script(args)

        print('\nCancelled.')
        exit()
