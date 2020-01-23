import os
import random


def control_randomness(seed, libs=None):
    """
    Sets the seed to main random library
    Args:
        seed:
        libs: list of libs to set the seed. By default, Torch and TensorFlow.
          The Numpy and random seeds are always set, regardless of the value of libs.
    """
    libs = libs or ["torch", "tensorflow"]

    random.seed(seed)
    # NUMPY
    try:
        import numpy as np
        np.random.seed(seed)
    except:
        pass

    # TORCH
    if "torch" in libs:
        try:
            import torch
            torch.manual_seed(seed)

            # Commented for performance issues...
            # c.f. https://pytorch.org/docs/1.1.0/notes/randomness.html#cudnn
            # torch.backends.cudnn.deterministic = True
            # torch.backends.cudnn.benchmark = False
        except:
            pass

    if "tensorflow" in libs:
        try:
            import tensorflow as tf
            tf_version = tf.__version__.split('.')
            if tf_version[0] == '1':
                # TENSORFLOW 1
                tf.compat.v1.set_random_seed(seed)
            elif tf_version[0] == '2':
                # TENSORFLOW 2
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
