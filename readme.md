```
 _______  _____  ____  _____  
|_   __ \|_   _||_   \|_   _| 
  | |__) | | |    |   \ | |   
  |  ___/  | |    | |\ \| |   
 _| |_    _| |_  _| |_\   |_  
|_____|  |_____||_____|\____| 

Project INitializer.
```

CLI to automate create of projects and scripts.

## Installation

Clone the repository then install the pin package.

```
pip install --upgrade git+https://github.com/bdvllrs/pin.git@v0.0.2
```

## Use the CLI

### Create new project

Go to the folder to build the project and execute
``` 
pin create PROJECT_NAME
```

A new project with the structure 
```
PROJECT_NAME/
    PROJECT_NAME/
        ...
    config/
    builds/
    setup.py
```

will be created.

### Add a new script
```
pin script add SCRIPT_NAME [-t TEMPLATE_NAME]
```

#### Available templates
The default template is `default`.
Also available: `torch`. 

You can also give a relative or absolute path towards a personal template.

#### Template semantics
They are python files with `.tpl` extension. You can access to the meta variables:
- `SCRIPT_NAME`: name of the script
- `PROJECT_NAME`: name of the project

You can unse them by using `%SCRIPT_NAME%` in the file.

## Some utils

### Constants
```python
from pin import DEBUG
```

The `DEBUG` constant indicates if a `PIN_DEBUG` environment variable has been set to `1`.

### Function for experiments
```python
from pin import control_randomness, set_cuda_device
```

- `control_randomness(seed)` sets the seed to the packages: random, numpy, torch, tensorflow.
- `set_cuda_device(device_number)` configures the environment variables `CUDA_DEVICE_ORDER` and `CUDA_VISIBLE_DEVICES`.

### Metrics and Writers
```python
from pin import SummaryWriter, Metrics
```
- `SummaryWriter` mixes sacred metric handling and tensorboard.
- `Metrics` counter for metrics.
