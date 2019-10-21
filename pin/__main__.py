import os
import argparse
import shutil
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[0]

possible_commands = ["create", "add_script"]


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
    setup_content = f"""from setuptools import find_packages, setup

setup(name='{preferences['name']}',
      version='{preferences['version']}',
      install_requires=[],
      packages=find_packages())\n
"""
    with open(base_path / "setup.py", "w") as setup_file:
        setup_file.write(setup_content)
    os.mkdir(base_path / preferences['name'])


def build_base_lib(base_path, preferences):
    os.mkdir(base_path / preferences['lib_name'])
    os.mkdir(base_path / preferences['lib_name'] / "utils")
    constants_content = f"""from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]
"""
    with open(base_path / preferences['name'] / "utils/constants.py", "w") as constants_file:
        constants_file.write(constants_content)


def script_create_project(args):
    preferences = get_preferences()

    base_path = Path(os.getcwd()) / preferences['lib_name']

    os.mkdir(base_path)

    build_config(base_path, preferences)
    build_builds(base_path, preferences)
    build_setup(base_path, preferences)
    build_base_lib(base_path, preferences)

    print(f"Project successfully created in {base_path}")


def script_add_script(args):
    base_path = Path(os.getcwd())
    project_name = str(base_path).split('/')[-1]
    project_name = get_prompt("Project name", project_name)
    script_name = get_prompt("Script name", "main")
    script_folder = get_prompt("Script folder", "scripts")

    script_content = f"""from pin.experiments import control_randomness, set_cuda_device
from pin.sacred import init_and_get_experiment
from {project_name}.utils.constants import PROJECT_DIR

ex = init_and_get_experiment(exp_name="{script_name}",
                             project_directory=PROJECT_DIR,
                             configs=["main.yaml"])


@ex.automain
def {script_name}(_run, _seed, _log, cuda, cuda_device):
    # Set randomness
    control_randomness(_seed)
    # Set available cuda devices to use
    set_cuda_device(cuda_device)

    device = torch.device('cpu')
    if cuda and torch.cuda.is_available():
        print("Using CUDA.")
        device = torch.device('cuda') 
    
    # TODO
"""
    with open(base_path / script_folder / (script_name + ".py"), 'w') as script_file:
        script_file.write(script_content)
    print(f"Script {script_name} successfully created.")


if __name__ == "__main__":
    args = get_arguments()

    if args.command == "create":
        script_create_project(args)
    elif args.command == "add_script":
        script_add_script(args)
    else:
        print(f"Command incorrect. Choose among {', '.join(possible_commands)}.")
