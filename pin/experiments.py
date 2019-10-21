import os
import random
from datetime import datetime

import numpy as np
import torch


def get_exp_id(run_id):
    """
    Generate an experiment id
    Args:
        run_id:
    """
    if run_id is not None:
        return run_id
    else:
        return datetime.now().strftime("%m-%d-%Y_%H-%M-%S")


def control_randomness(seed):
    """
    Sets the seed to main random library
    Args:
        seed:
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    # Commented for performance issues...
    # c.f. https://pytorch.org/docs/1.1.0/notes/randomness.html#cudnn
    # torch.backends.cudnn.deterministic = True
    # torch.backends.cudnn.benchmark = False


def set_cuda_device(device_number):
    """
    Set available cuda devices
    Args:
        device_number:
    """
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = str(device_number)
