import numpy as np


class SummaryWriter:
    """
    Logger to log on tensorboard and sacred.
    API follows the tensorboard SummaryWriter API with only a subset of the functions available.
    """
    def __init__(self, tensorboard_writer=None, sacred_run=None):
        """
        Args:
            tensorboard_writer:
            sacred_run: _run variable from sacred
        """
        self.tensorboard_writer = tensorboard_writer
        self.sacred_writer = sacred_run

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


class Metrics:
    def __init__(self, writer=None, print_every=50, first_epoch=0, prefix=None):
        self.writer = writer

        self.metrics = dict()
        self.buffer = dict()
        self.running_avg = dict()
        self.raw_prefix = "" if prefix is None else prefix
        self.prefix = "" if prefix is None else prefix + " "

        self.current_step = 0
        self.epoch = first_epoch
        self.print_every = print_every

    def add(self, key, value):
        if key in self.buffer.keys():
            self.buffer[key].append(value)
        else:
            self.buffer[key] = [value]

        if key not in self.metrics.keys():
            self.metrics[key] = []
            if key not in self.running_avg.keys():
                self.running_avg[key] = []

    def new_epoch(self):
        self.compute_average()
        self.print()

        for key in self.metrics.keys():
            self.metrics[key] = []
            self.running_avg[key] = []

        self.current_step = 0
        self.epoch += 1

    def step(self, content_dict=None):
        if content_dict is None:
            content_dict = dict()
        for key, value in content_dict.items():
            self.add(key, value)

        self.current_step += 1

        if not self.current_step % self.print_every:
            self.compute_average()
            self.print()

    def compute_average(self):
        for key, values in self.buffer.items():
            average = np.mean(values)
            self.running_avg[key].append(average)
            self.metrics[key].append(average)
            self.buffer[key] = []

    def print(self):
        msg = f"{self.prefix}[Epoch {self.epoch}] [Step {self.current_step}]: "
        msg += ", ".join([f"{key}: {self.metrics[key][-1]:0.3f} ({self.running_avg[key][-1]:0.3f})"
                          for key in self.running_avg.keys()])
        print(msg)

        if self.writer is not None:
            for key in self.metrics.keys():
                if len(self.metrics[key]):
                    self.writer.add_scalar(self.raw_prefix + "_" + key, self.metrics[key][-1])

    def __getattr__(self, item):
        return np.mean(self.metrics[item])

