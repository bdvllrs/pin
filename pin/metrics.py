import numpy as np


class Metrics:
    """
    Handle metrics, computes averages, log in Summary writer and print in console.
    """

    def __init__(self, writer=None, print_every=50, first_epoch=0, prefix=None, no_op=False):
        """
        Args:
            writer: SummaryWriter object if want to log in Tensorboard.
            print_every: Frequency to write content of metrics.
            first_epoch:
            prefix: A prefix to set when logging.
            no_op: If true, acts as no_op
        """
        self.writer = writer

        self.metrics = dict()
        self.buffer = dict()
        self.running_avg = dict()
        self.prefix = "" if prefix is None else prefix

        self.current_step = 0
        self.epoch = first_epoch
        self.print_every = print_every
        self.no_op = no_op

    def add(self, key, value):
        """
        Add a value in the buffer
        Args:
            key:
            value:

        Returns:
        """
        if not self.no_op:
            self.extend(key, [value])

    def extend(self, key, values):
        if not self.no_op:
            if key in self.buffer.keys():
                self.buffer[key].extend(values)
            else:
                self.buffer[key] = values

            if key not in self.metrics.keys():
                self.metrics[key] = []
            if key not in self.running_avg.keys():
                self.running_avg[key] = []

    def new_epoch(self):
        """
        Starts a new epoch: Computes averages and empty buffers.
        """
        if not self.no_op:
            for key in self.metrics.keys():
                self.metrics[key] = []
                self.running_avg[key] = []

            self.current_step = 0
            self.epoch += 1

    def step(self, step=None, content_dict=None, force_print=False):
        """
        Call step every at the end of every iteration. Will print or log if
        the step % print_every is 1.
        Args:
            step: current step. If none, will keep current count.
            content_dict: Some additional metrics to add before logging.
            force_print: if print is False, will only print every self.print_every iterations. Otherwise will print now.
        """
        if not self.no_op:
            if content_dict is None:
                content_dict = dict()
            for key, value in content_dict.items():
                self.add(key, value)

            if step is not None:
                self.current_step = step
            else:
                self.current_step += 1

            if force_print or not self.current_step % self.print_every:
                self.compute_average()
                self.print()

    def compute_average(self):
        if not self.no_op:
            for key, values in self.buffer.items():
                average = np.mean(values)
                self.running_avg[key].append(average)
                self.metrics[key].extend(values)
                self.buffer[key] = []

    def print(self):
        if not self.no_op:
            msg = f"{self.prefix} [Epoch {self.epoch}] [Step {self.current_step}]: "
            msg += ", ".join([f"{key}: {self.metrics[key][-1]:0.3f} ({self.running_avg[key][-1]:0.3f})"
                              for key in self.running_avg.keys()])
            print(msg)

            if self.writer is not None:
                for key in self.metrics.keys():
                    if len(self.metrics[key]):
                        self.writer.add_scalar(self.prefix + "_" + key, self.running_avg[key][-1], self.current_step)

    def __getitem__(self, item):
        if self.no_op:
            return None
        return np.mean(self.metrics[item])