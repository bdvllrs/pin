import os

import torch
from typing import Union
from pathlib import Path

path_type = Union[Path, str]


class Artifact:
    def __init__(self, path: path_type, name: str, num_kept_versions: int = 10):
        self.path = path if isinstance(path, Path) else Path(path)
        self.name = name
        self.version = 1
        self.best_version = None
        self.best_version_value = None
        self.artifact = None
        self.num_kept_versions = num_kept_versions

        self.saved_versions = dict()

    def update(self, artifact):
        self.artifact = artifact

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
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
        file_name = self.path / self.name.format(version=self.version)
        self.save(file_name, **kwargs)
        self.saved_versions[self.version] = file_name
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
        raise NotImplementedError

    def load(self, filename, *params, version="best"):
        raise NotImplementedError

    def clean(self):
        to_remove = sorted(self.saved_versions.keys())[:len(self.saved_versions.keys()) - self.num_kept_versions]
        for index in to_remove:
            os.remove(self.saved_versions[index])
            del self.saved_versions[index]


class TorchModelArtifact(Artifact):
    def save(self, filename, **kwargs):
        torch.save(self.artifact, filename)

    def load(self, filename, models, version="best"):
        file_name = self.path / filename.format(version=version)
        loaded_dicts = torch.load(file_name)
        is_not_dict = type(models) is not dict and type(loaded_dicts) is not dict
        if is_not_dict:
            models = dict(default=models)
            loaded_dicts = dict(default=loaded_dicts)
        for key, model in models:
            if key in loaded_dicts.keys():
                model.load_state_dict(loaded_dicts[key])
            else:
                print(f"{key} is not in the checkpoint. Skipping.")
        return models["default"] if is_not_dict else models
