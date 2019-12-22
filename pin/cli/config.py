import os
from pathlib import Path

import click
from ruamel.yaml import YAML

from pin.cli.utils import find_root_folder
from pin.config import configs_in, import_matches


def make_dict_from_dot_path(dot_path, value):
    if not len(dot_path):
        return value
    key = dot_path.pop(0)
    return {key: make_dict_from_dot_path(dot_path, value)}


def is_dotted_key_in_dict(dotted_key, d):
    if not len(dotted_key):
        return False
    if len(dotted_key) == 1:
        return dotted_key[0] in d
    key = dotted_key.pop(0)
    return key in d and is_dotted_key_in_dict(dotted_key, d[key])


@click.group("config", help="Manages configurations.")
def config_group():
    """
    Base for the config group.
        $ pin config --help
    to list all the available commands.
    """
    pass


@config_group.command("init", help="Initialize empty configurations.")
def init_config():
    """
    Analysis missing configuration values, creates and fills
     missing configuration files
    """
    yaml = YAML()
    yaml.preserve_quotes = True

    base_path = find_root_folder(Path(os.getcwd()))
    len_conf_base = len(str(base_path / 'config')) + 1
    for config_path, config in configs_in(base_path / 'config'):
        # source_file_name = config_path[len_conf_base:]
        config_root_path = Path('/'.join(config_path.split('/')[:-1]))
        for match in import_matches(config):
            import_path = config_root_path / (match.group(1).strip().replace('.', '/') + ".yaml")
            import_var = []
            if match.group(3) is not None:
                import_var = match.group(3).strip().split('.')
            target_file_name = str(import_path)[len_conf_base:]
            # Look if file does not exists. And ask to create it.
            if not import_path.exists():
                if click.confirm(f"The configuration file `{target_file_name}` "
                                 "does not exist. Do you want to create it?",
                                 default=True):
                    with open(import_path, 'w') as f:
                        f.write('')
            # Ask to add missing configuration keys.
            if import_path.exists() and len(import_var):
                with open(import_path, 'r') as yaml_file:
                    yaml_content = yaml.load(yaml_file)

                if yaml_content is None:
                    yaml_content = dict()

                if not is_dotted_key_in_dict(import_var, yaml_content):
                    prompted_val = click.prompt(f"The configuration file `{target_file_name}` "
                                                f"is missing the key `{match.group(3).strip()}`. "
                                                "Fill it with")
                    # TODO: We assume that each config file is a dict yaml.
                    #  To be adapted for list configs.
                    sub_dict = make_dict_from_dot_path(import_var, prompted_val)
                    yaml_content.update(sub_dict)
                    with open(import_path, 'w') as f:
                        yaml.dump(yaml_content, f)
