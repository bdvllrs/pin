import os
from pathlib import Path
from typing import Union
import re

path_type = Union[Path, str]


class Artifact:
    """"
    Base class for artifacts.
    """

    def __init__(self, path: path_type, name: str,
                 num_kept_versions: int = 10,
                 debug: bool = False):
        """

        Args:
            path: base path to save the artifact
            name: name of the artifact. Must montain the {version} token to update.
                Example: "model_artifact_{version}.ext"
            num_kept_versions: Number of kept version of the artifact. Default: 10
        """
        self.path = path if isinstance(path, Path) else Path(path)
        self.name = name
        self.version = 1
        self.best_version = None
        self.best_version_value = None
        self.artifact = None
        self.num_kept_versions = num_kept_versions
        self.debug = debug

        self.saved_versions = dict()

    def update(self, artifact):
        """
        Update the current artifact.
        Args:
            artifact:

        Returns:

        """
        self.artifact = artifact

    def __enter__(self):
        """
        Use it as a context manager to save the updated artifact if an error occurs.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None and not self.debug:
            file_name = self.path / self.name.format(version="recovery")
            self.save(file_name)

    def checkpoint(self, metric=None, **kwargs):
        """
        Saves a checkpoint to self.path / name
        Args:
            name: name that will be formatted. Can have the value "version".
            metric: a value to inform how good this artifact is (higher is better).
            **kwargs:

        Returns:

        """
        if not self.debug:
            file_name = self.path / self.name.format(version=self.version)
            self.save(file_name, **kwargs)
            self.clean()
            self.version += 1
            if self.is_best(metric):
                file_name = self.path / self.name.format(version="best")
                self.save(file_name, **kwargs)

    def is_best(self, metric=None):
        """
        Returns if the new artifact is best or not.
        Args:
            metric:

        Returns:

        """
        if metric is not None:
            if self.best_version is None or self.best_version_value < metric:
                self.best_version = self.version
                self.best_version_value = metric
                return True
        return False

    def save(self, filename, **kwargs):
        """
        Save the model
        Args:
            filename:
            **kwargs:

        Returns:

        """
        raise NotImplementedError

    def load(self, *params, version="best"):
        """
        Load an artifact
        Args:
            *params:
            version:

        Returns:

        """
        raise NotImplementedError

    def resume(self, *params, use_recovery=True):
        """
        Same as load, but infers the version to load by taking either the recovery model if it exists, or the latest
         model version.
        Args:
            *params:
            use_recovery: if False, will not try to use the recovery model. Defaults to True

        Returns:

        """
        models = os.listdir(self.path)
        if use_recovery and self.name.format(version="recovery") in models:
            return self.load(*params, version="recovery")
        latest_model = 1
        for model in models:
            match = re.match(self.name.format(version="([0-9]+)"), model)
            if match:
                model_version = match.group(1)
                if model_version.isdigit() and latest_model < int(model_version):
                    latest_model = int(model_version)
        return self.load(*params, version=str(latest_model))

    def clean(self):
        if os.path.isfile(self.path / self.name.format(version="recovery")):
            os.remove(self.path / self.name.format(version="recovery"))
        to_remove = sorted(self.saved_versions.keys())[:len(self.saved_versions.keys()) - self.num_kept_versions]
        for index in to_remove:
            os.remove(self.saved_versions[index])
            del self.saved_versions[index]


class TorchModelArtifact(Artifact):
    @staticmethod
    def _get_state_dict(item):
        if hasattr(item, "state_dict"):
            state_dict = item.state_dict()
        else:
            state_dict = item
        return state_dict

    def save(self, filename, **kwargs):
        import torch

        artifact = self.artifact
        if type(artifact) != dict:
            saved_artifact = self._get_state_dict(artifact)
        else:
            saved_artifact = dict()
            for key, item in artifact.items():
                saved_artifact[key] = self._get_state_dict(item)
        torch.save(saved_artifact, filename)

    def load(self, models, version="best"):
        """
        Load the artifact
        Args:
            models: dict of models. Keys should be the same as the saved keys of the artifacts.
            version: version to load

        Returns: dicts of loaded models

        """
        import torch

        file_name = self.path / self.name.format(version=version)
        loaded_dicts = torch.load(file_name)
        is_not_dict = type(models) is not dict and type(loaded_dicts) is not dict
        if is_not_dict:
            models = dict(default=models)
            loaded_dicts = dict(default=loaded_dicts)
        for key, model in models.items():
            if key in loaded_dicts.keys():
                if hasattr(model, "load_state_dict"):
                    model.load_state_dict(loaded_dicts[key])
                else:
                    models[key] = loaded_dicts[key]
            else:
                print(f"{key} is not in the checkpoint. Skipping.")
        return models["default"] if is_not_dict else models
