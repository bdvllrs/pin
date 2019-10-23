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
pip install --upgrade git+https://github.com/bdvllrs/pin.git
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
pin add script SCRIPT_NAME
```

## Some utils

In `pin/sacred/utils.py`. Documentation coming...

