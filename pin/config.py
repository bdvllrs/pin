import os
import re
from pathlib import Path
from typing import Union

from omegaconf import OmegaConf, DictConfig, ListConfig

config_type = Union[DictConfig, ListConfig]


def load_config(path, imports=True, to_container=False):
    """
    Load configuration.
    Args:
        path: path to the configuration
        imports: if imports should be resolved. Defaults to True.
        to_container: if True will return a dict or list according to the config type. Otherwise
          will return the omegaconf object.

    Returns: OmegaConf
    """
    conf = OmegaConf.load(path)
    if imports:
        resolve_imports(path, conf)
    if to_container:
        return OmegaConf.to_container(conf, resolve=True)
    return conf


def get_nested_key_in_config(conf, keys):
    """
    Returns the value of a nested key from an OmegaConf conf.
    Args:
        conf: configuration
        keys (list): nested key. For instance ['key1', 'key2'] will return conf['key1']['key2'].
    Returns: the associated value.
    """
    if not len(keys):
        return conf
    cur_var = keys.pop(0)
    if cur_var in conf:
        return get_nested_key_in_config(conf[cur_var], keys)
    raise ValueError(f"{cur_var} is not in the configuration.")


def update_dict_from_nested_key(config, nested_key, value):
    if not len(nested_key):
        return
    if len(nested_key) == 1:
        config[nested_key[0]] = value
    key = nested_key.pop(0)
    update_argv_from_arguments(config[key], nested_key, value)


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


def _update_values(source_path, path, item, conf: config_type, sub_conf):
    """
    Update a sub_conf str if contains an auto import line
    Args:
        source_path: source path
        path:
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
            resolve_imports(str(source_path / source), imported)
            try:
                content = get_nested_key_in_config(imported, var)
            except ValueError:  # More specific error message with path of the config file.
                raise ValueError(f"{'.'.join(var)} is not in {source}.")
            # Recursively import
            if isinstance(content, str):
                # We just replace part of the string of the match
                conf[item] = conf[item].replace(match.group(0), content.strip())
            else:
                conf[item] = content
    elif isinstance(sub_conf, (DictConfig, ListConfig)):
        resolve_imports(path, sub_conf)


def resolve_imports(path, conf: config_type):
    """
    Replaces inplace auto imports in the conf
    Args:
        path:
        conf: OmegaConf
    """
    source_path = Path('/'.join(path.split('/')[:-1]))
    original_conf = conf.copy()
    if isinstance(conf, DictConfig):
        for item in resolve_order(original_conf):
            first_index = item.split('.')[0]
            _update_values(source_path, path, first_index, conf, conf[first_index])
    elif isinstance(conf, ListConfig):
        for item, sub_conf in enumerate(original_conf):
            _update_values(source_path, path, item, conf, sub_conf)


def get_keys_to_resolve(conf, prefix=None):
    if prefix is None:
        prefix = []
    items = []
    for item, sub_conf in conf.items():
        new_prefix = prefix + [item]
        if isinstance(sub_conf, DictConfig):
            items.extend(get_keys_to_resolve(sub_conf, new_prefix))
        else:
            items.append(".".join(new_prefix))
    return items


def resolve_order(conf):
    """
    Yields the order to resolve the imports
    Args:
        conf:
    """
    keys = list(get_keys_to_resolve(conf))
    return sorted(keys, key=lambda x: len(x.split('.')))


def configs_in(base_path):
    """
    Yields all configurations in a given path (recursively).
    Args:
        base_path:
    Yields: configuration contents
    """
    for dir_path, dir_names, file_names in sorted(os.walk(base_path), key=lambda x: x[0]):
        for file in sorted(file_names):
            path = os.path.join(dir_path, file)
            with open(path, 'r') as config_file:
                yield path, config_file.read()


def update_argv_from_arguments(args, conf, path):
    source_path = Path('/'.join(path.split('/')[:-1]))
    conf = conf.copy()
    # Check that its a sacred valid cli input
    if len(args) > 1 and args[1] == 'with':
        for k, arg in enumerate(args[2:], 2):
            for match in re.finditer(r"'?([^']*)\s?=\s?([^']*)'?", arg):
                if match.group(1) is not None and match.group(2) is not None:
                    item, value = match.group(1), match.group(2)
                    update_dict_from_nested_key(conf, item.split('.'), value)
                    _update_values(source_path, path, item, conf, value)
                    args[k] = f"'{item}={conf[item]}'"
