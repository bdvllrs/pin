import os
from typing import Union
import re
from omegaconf import OmegaConf, DictConfig, ListConfig
from pathlib import Path

config_type = Union[DictConfig, ListConfig]


def get_content_from_sub_var(conf, var_path, path):
    if not len(var_path):
        return conf
    cur_var = var_path.pop(0)
    if cur_var in conf:
        return get_content_from_sub_var(conf[cur_var], var_path, path)
    raise ValueError(f"{cur_var} is not in the configuration {path}.")


def import_matches(conf):
    """
    Yields all regex matches of imports in a given config str.
    Args:
        conf (str):
    Yields: regex matches
    """
    # Get items of the form @{path:var} where path can be words, ., %, _, \, -.
    allowed_characters = r"[\w\.%_ \\,-]"
    regex = r"@{(" + allowed_characters + r"+)(:(" + allowed_characters + r"*?))?}"
    for match in re.finditer(regex, conf):
        yield match


def update_values(source_path, path, item, conf: config_type, sub_conf):
    """
    Update a sub_conf str if contains an auto import line
    Args:
        source_path: source path
        item: item (or index)
        conf: original configuration
        sub_conf: sub configuration
    """
    if isinstance(sub_conf, str):
        for match in import_matches(sub_conf):
            var = []
            if match.group(1) is not None and match.group(3) is None:
                source = match.group(1).strip()
            elif match.group(3) is not None:
                source = match.group(1).strip()
                var = match.group(3).strip().split('.')
            else:
                raise ValueError(f"{sub_conf} has a syntax error.")
            source = source.replace('.', '/') + '.yaml'
            imported = OmegaConf.load(str(source_path / source))
            content = get_content_from_sub_var(imported, var, source)
            new_source_path = Path('/'.join(str(source_path / source).split('/')[:-1]))
            # Recursively import
            resolve_imports(new_source_path, source, content)
            if isinstance(content, str):
                # We just replace part of the string of the match
                conf[item] = conf[item].replace(match.group(0), content)
            else:
                conf[item] = content
    elif isinstance(sub_conf, (DictConfig, ListConfig)):
        resolve_imports(source_path, path, sub_conf)


def resolve_imports(source_path, path, conf: config_type):
    """
    Replaces inplace auto imports in the conf
    Args:
        source_path: path to the conf
        conf: omegaconf
    """
    if isinstance(conf, DictConfig):
        for item, sub_conf in conf.items():
            update_values(source_path, path, item, conf, sub_conf)
    elif isinstance(conf, ListConfig):
        for item, sub_conf in enumerate(conf):
            update_values(source_path, path, item, conf, sub_conf)


def get_config(filename, imports=True):
    source_path = Path('/'.join(filename.split('/')[:-1]))
    conf = OmegaConf.load(filename)
    if imports:
        resolve_imports(source_path, filename, conf)
    return conf


def configs_in(base_path):
    """
    Yields all configurations in a given path (recursively).
    Args:
        base_path:
    Yields: configuration contents
    """
    for dir_path, dir_names, file_names in os.walk(base_path):
        for file in file_names:
            path =  os.path.join(dir_path, file)
            with open(path, 'r') as config_file:
                yield path, config_file.read()