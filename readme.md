# Plotster
From film poster to its plot.

## Installation

Clone the repository then install the plotster package.

```
pip install --user -e .
```


## Data
The data structure is 

```
data/
    poster/
        poster_2.jpg
        poster_3.jpg
        ...
    movie_data.csv
``` 


## Config

The default configurations are stored in `config/default`.

**Never** change the values in the default config (this folder is synced with GitHub). Instead, copy
the file in the `config` folder and replace it here. The values
in this file will be used instead of the default file.

Example: to change the default `path` in the `config/default/data.yaml` file:
copy `config/default/data.yaml` to `config/data.yaml` and change the values there.