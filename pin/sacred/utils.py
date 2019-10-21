from ..constants import DEBUG
from pathlib import Path

import yaml
from sacred import Experiment, SETTINGS
from sacred.observers import FileStorageObserver
from sacred.observers import MongoObserver
from sacred.utils import apply_backspaces_and_linefeeds


def add_dir_sources(experiment, path, allowed_exts=None):
    """
    Add a directory to sacred source files
    Args:
        experiment:
        path:
        allowed_exts:
    """
    allowed_exts = ['.py'] if allowed_exts is None else allowed_exts
    path = Path(path) if not isinstance(path, Path) else path
    for sub_file in path.iterdir():
        if sub_file.is_dir():
            add_dir_sources(experiment, sub_file)
        elif sub_file.suffix in allowed_exts:
            experiment.add_source_file(sub_file)


def get_config(root_path, filename):
    if not isinstance(root_path, Path):
        root_path = Path(root_path)
    file = root_path / filename
    if not file.exists():
        file = root_path / "default" / filename
    with open(file, "r") as f:
        conf = yaml.load(f)
    return conf


def get_sacred_conf(config_root):
    sacred_conf = get_config(config_root / "config", "sacred.yaml")
    if 'sacred' not in sacred_conf:
        return None
    return sacred_conf


def init_and_get_experiment(exp_name, project_directory, ingredients=None,
                            configs=None, debug_mode=None,
                            interactive=False):
    """
    Initialize sacred configs and get the experiment object
    Args:
        debug_mode: Overrides the DEBUG const
        exp_name: experiment name
        ingredients: ingredients to load
        configs: config files to load
        interactive: if interactive mode
    Returns: The Experiment instance
    """
    debug_mode = DEBUG if debug_mode is None else debug_mode

    SETTINGS.CAPTURE_MODE = 'sys'
    ingredients = ingredients if ingredients is not None else []
    ex = Experiment(exp_name, ingredients=ingredients, interactive=interactive)

    sacred_conf = get_sacred_conf(project_directory)
    if sacred_conf is None:
        print("The sacred.yaml file is not configured. Using debug mode.")
        debug_mode = True
    ex.captured_out_filter = apply_backspaces_and_linefeeds  # for tqdm

    # Add observers
    # Mongo DB
    if not debug_mode and sacred_conf['sacred']['observer'] == "mongodb":
        observer = MongoObserver(sacred_conf['sacred']['mongodb']['url'],
                                 sacred_conf['sacred']['mongodb']['db_name'])
        ex.observers.append(observer)
        print("Added MongoDB Observer,", sacred_conf['sacred']['mongodb'])

    # File Storage
    elif not debug_mode and sacred_conf['sacred']['observer'] == "file_storage":
        observer = FileStorageObserver(sacred_conf['sacred']['file_storage']['path'])
        ex.observers.append(observer)
        print("Added File Storage Observer in", sacred_conf['sacred']['file_storage']['path'])

    for file in configs:
        ex.add_config(get_config(project_directory / "config", file))

    if debug_mode:
        ex.add_config(get_config(project_directory / "config", "debug.yaml"))
    return ex