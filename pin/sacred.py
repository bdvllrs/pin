import inspect
import sys
from pathlib import Path

from munch import Munch
from sacred import Experiment as SacredExperiment, SETTINGS
from sacred.config.custom_containers import ReadOnlyDict
from sacred.observers import FileStorageObserver
from sacred.observers import QueuedMongoObserver
from sacred.utils import apply_backspaces_and_linefeeds

from pin.config import load_config, update_argv_from_arguments
from pin.constants import DEBUG

dict_types = [dict, ReadOnlyDict]


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


def get_sacred_conf(config_root):
    sacred_conf = load_config(str(config_root / "config/sacred.yaml"))
    if 'sacred' not in sacred_conf:
        return None
    return sacred_conf


class Experiment(SacredExperiment):
    def __init__(self, exp_name, project_directory, ingredients=None,
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
        super().__init__(exp_name, ingredients=ingredients, interactive=interactive)

        add_dir_sources(self, project_directory)

        sacred_conf = get_sacred_conf(project_directory)
        if sacred_conf is None:
            print("The sacred.yaml file is not configured. Using debug mode.")
            debug_mode = True
        self.captured_out_filter = apply_backspaces_and_linefeeds  # for tqdm

        # Add observers
        # Mongo DB
        observers = sacred_conf['sacred']['observer']
        if type(observers) == str:
            observers = [observers]
        if not debug_mode and  "mongodb" in observers:
            observer = QueuedMongoObserver(url=sacred_conf['sacred']['mongodb']['url'],
                                           db_name=sacred_conf['sacred']['mongodb']['db_name'])
            self.observers.append(observer)
            print("Added MongoDB Observer,", sacred_conf['sacred']['mongodb'])

        # File Storage
        elif not debug_mode and "file_storage" in observers:
            observer = FileStorageObserver(sacred_conf['sacred']['file_storage']['path'])
            self.observers.append(observer)
            print("Added File Storage Observer in", sacred_conf['sacred']['file_storage']['path'])

        for file in configs:
            path = str(project_directory / "config" / file)
            config = load_config(path, to_container=True)
            update_argv_from_arguments(sys.argv, config, path)
            # FIXME: what if the config is a ListConf?
            #  Same for the next one.
            self.add_config(config)

        if debug_mode:
            path = str(project_directory / "config/debug.yaml")
            config = load_config(path, to_container=True)
            update_argv_from_arguments(sys.argv, config, path)
            self.add_config(config)


def munchify(function):
    def wrapper(*params, **kwargs):
        new_params = []
        new_kwargs = dict()
        for param in params:
            if type(param) in dict_types:
                new_params.append(Munch.fromDict(param))
            else:
                new_params.append(param)
        for key, item in kwargs.items():
            if type(item) in dict_types:
                new_kwargs[key] = Munch.fromDict(item)
            else:
                new_kwargs[key] = item
        function(*new_params, **new_kwargs)

    sig = inspect.signature(function)
    sig = sig.replace(parameters=tuple(sig.parameters.values()))
    wrapper.__signature__ = sig
    wrapper.__module__ = function.__module__

    return wrapper
