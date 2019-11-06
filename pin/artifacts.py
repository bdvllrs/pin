import torch
from typing import Union
from pathlib import Path

path_type = Union[Path, str]


class Artifacts:
    def __init__(self, path: path_type):
        self.path = path if isinstance(path, Path) else Path(path)
        self.version = 1
        self.best_version = None
        self.best_version_value = None

    def checkpoint(self, name, artifact, metric=None, **kwargs):
        """
        Saves a checkpoint to self.path / name
        Args:
            name: name that will be formatted. Can have the value "version".
            artifact: artifact to save
            metric: a value to inform how good this artifact is (higher is better).
            **kwargs:

        Returns:

        """
        file_name = self.path / name.format(version=self.version)
        self.save(file_name, artifact, **kwargs)
        self.version += 1
        if self.is_best(metric):
            file_name = self.path / name.format(version="best")
            self.save(file_name, artifact, **kwargs)

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

    def save(self, filename, artifact, **kwargs):
        raise NotImplementedError

    def load(self, filename, *params, version="best"):
        raise NotImplementedError


class TorchModelArtifact(Artifacts):
    def save(self, filename, model, **kwargs):
        torch.save(model, filename)

    def load(self, filename, model, version="best"):
        file_name = self.path / filename.format(version=version)
        model.load_state_dict(torch.load(file_name))
