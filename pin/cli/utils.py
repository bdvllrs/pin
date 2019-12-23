import os
import shutil
from pathlib import Path

import click

from pin.sacred import get_sacred_conf


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def load_template(template_name, **vars):
    base_path = Path(os.getcwd())
    if template_name[-4:] != ".tpl":
        template_name += ".tpl"
    template_file_path = PROJECT_DIR / "templates" / template_name

    if (base_path / template_name).exists():
        template_file_path = base_path / template_name
    elif Path(template_name).exists():
        template_file_path = Path(template_name)
    elif not template_file_path.exists():
        raise click.ClickException("Template file not found.")

    with open(template_file_path, "r") as template_file:
        template_content = template_file.read()
    for var, value in vars.items():
        template_content = template_content.replace(f"%{var}%", value)
    return template_content


def find_root_folder(base_path):
    if (base_path / "setup.py").exists():
        return base_path
    if not len(base_path.parents):
        return False
    return find_root_folder(base_path.parent)


def find_and_get_sacred_conf(base_path):
    root_folder = find_root_folder(base_path)
    if root_folder:
        return get_sacred_conf(root_folder)
    return None


PROJECT_DIR = Path(__file__).resolve().parents[1]


def splash_screen():
    return """ _______  _____  ____  _____  
|_   __ \|_   _||_   \|_   _| 
  | |__) | | |    |   \ | |   
  |  ___/  | |    | |\ \| |   
 _| |_    _| |_  _| |_\   |_  
|_____|  |_____||_____|\____| 

Project INitializer.
"""