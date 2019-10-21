import os
import argparse
import shutil
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[0]


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
    preferences['version'] = get_prompt("Project version", "0.0.1")
    preferences['description'] = get_prompt("Project description", "")
    preferences['config'] = get_prompt("Configuration folder", "config")
    preferences['build'] = get_prompt("Build folder", "builds")

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


if __name__ == "__main__":
    args = get_arguments()

    preferences = get_preferences()

    base_path = Path(os.getcwd()) / preferences['name']

    os.mkdir(base_path)

    build_config(base_path, preferences)
    build_builds(base_path, preferences)
    build_setup(base_path, preferences)
