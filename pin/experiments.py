import os
import random


def control_randomness(seed):
    """
    Sets the seed to main random library
    Args:
        seed:
    """
    random.seed(seed)
    # NUMPY
    try:
        import numpy as np
        np.random.seed(seed)
    except:
        pass

    # TORCH
    try:
        import torch
        torch.manual_seed(seed)

        # Commented for performance issues...
        # c.f. https://pytorch.org/docs/1.1.0/notes/randomness.html#cudnn
        # torch.backends.cudnn.deterministic = True
        # torch.backends.cudnn.benchmark = False
    except:
        pass

    # TENSORFLOW 1
    try:
        import tensorflow as tf
        tf.compat.v1.set_random_seed(seed)
    except:
        pass

    # TENSORFLOW 2
    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except:
        pass


def set_cuda_device(device_number):
    """
    Set available cuda devices
    Args:
        device_number:
    """
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = str(device_number)
