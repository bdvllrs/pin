```
 _______  _____  ____  _____  
|_   __ \|_   _||_   \|_   _| 
  | |__) | | |    |   \ | |   
  |  ___/  | |    | |\ \| |   
 _| |_    _| |_  _| |_\   |_  
|_____|  |_____||_____|\____| 

Project INitializer.
```

CLI to automate creation of projects and scripts.

I created this tool to remove all boilerplate I had to write when
starting a new project. It contains a CLI to create new projects and 
new scripts, and it also contains functions I often use.

## Installation

```
pip install --upgrade git+https://github.com/bdvllrs/pin.git
```

Or any last release.

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
        default/
    builds/
    setup.py
```

will be created.

#### Configs
The config folder contains a subfolder `config/default` containing default
configuration. To overwrite, copy the file in the `config` folder and
update those values.

When using a versioning system, it is recommended to only version the default
folder.

### Add a new script
```
pin script add SCRIPT_NAME [-t TEMPLATE_NAME]
```

#### Available templates
List templates using:
```
pin script templates
```

The default template is `default`.

You can also give a relative or absolute path towards a personal template.


### Start omniboard
```
pin omniboard
```
starts omniboard using the settings defined in the `sacred.yaml` file.
Works only if omniboard is already installed ([docs](https://vivekratnavel.github.io/omniboard/#/quick-start)).

#### Template semantics
They are python files with `.tpl` extension. You can access to the meta variables:
- `SCRIPT_NAME`: name of the script
- `PROJECT_NAME`: name of the project

You can unse them by using `%SCRIPT_NAME%` in the file.

## Some utils
Attention. Non exhaustive documentation.


### Sacred
I use sacred to log my experiments. The sacred functions are stored in:
```python
import pin.sacred
```

#### `init_and_get_experiment`
```python
ex = init_and_get_experiment(
        exp_name="EXPERIMENT_NAME",
        project_directory="/path/to/project/working/directory",
        ingredients=[],  # list of ingredients to load
        configs=[],  # list of config names to load from the config folder
        debug_mode=DEBUG,  # if True, no observer is added
        interactive=False  # if interactive session
    )
```
This initializes the experiment and loads config from the config folder
according to the wanted config names provided in the `configs` parameter.

It will try to load the config in the `config` folder. If it does not exist, 
it will load the file in the `config/default`.

#### `@munchify`
Changes all dictionary provided by sacred into [Munch](https://github.com/Infinidat/munch) objects.
Example to use:
```python
import sacred
import pin.sacred

ex = sacred.Experiment("test")

@ex.automain
@pin.sacred.munchify
def main(dict_config_entry):
    # config_entry will be a Munch object.
    pass
```

### Constants
```python
from pin import DEBUG
```

The `DEBUG` constant indicates if a `PIN_DEBUG` environment variable has been set to `1`.
This is useful to know when to add observers in a sacred experiment.

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

### Artifacts

