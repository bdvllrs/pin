# PIN

Create a new Python Project

## Installation

Clone the repository then install the pin package.

```
pip install --upgrade git+https://github.com/bdvllrs/pin.git@v0.0.1
```

## Use

### Create new project

Go to the folder to build the project and execute
``` 
python -m pin create
```

A new project with the structure 
```
project_name/
    project_name/
    config/
    builds/
    setup.py
```

will be created.

### Add a new script
```
python -m pin add_script
```
