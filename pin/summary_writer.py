import numpy as np


class SummaryWriter:
    """
    Logger to log on tensorboard and sacred.
    API follows the tensorboard SummaryWriter API with only a subset of the functions available.
    """

    def __init__(self, tensorboard_writer=None, sacred_run=None, no_op=False):
        """
        Args:
            tensorboard_writer:
            sacred_run: _run variable from sacred
            no_op: if True, acts as no op.
        """
        self.tensorboard_writer = None if no_op else tensorboard_writer
        self.sacred_writer = None if no_op else sacred_run

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def add_scalar(self, tag, scalar_value, global_step=None, walltime=None):
        if self.tensorboard_writer is not None:
            self.tensorboard_writer.add_scalar(tag, scalar_value, global_step, walltime)
        if self.sacred_writer is not None:
            self.sacred_writer.log_scalar(tag, scalar_value, global_step)

    def add_scalars(self, main_tag, tag_scalar_dict, global_step=None, walltime=None):
        if self.tensorboard_writer is not None:
            self.tensorboard_writer.add_scalars(main_tag, tag_scalar_dict, global_step, walltime)
        if self.sacred_writer is not None:
            for name, value in tag_scalar_dict.items():
                self.sacred_writer.log_scalar(f"{main_tag}_{name}", value, global_step)

    def add_embedding(self, mat, metadata=None, label_img=None, global_step=None, tag='default',
                      metadata_header=None):
        if self.tensorboard_writer is not None:
            self.tensorboard_writer.add_embedding(mat, metadata, label_img, global_step, tag, metadata_header)

    def add_figure(self, tag, figure, global_step=None, close=True, walltime=None):
        if self.tensorboard_writer is not None:
            self.tensorboard_writer.add_figure(tag, figure, global_step, close, walltime)

    def save_artifact(self, build, content_dict):
        pass

    def close(self):
        if self.tensorboard_writer is not None:
            self.tensorboard_writer.close()
