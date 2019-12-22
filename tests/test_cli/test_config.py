import os
import shutil

import pytest
from click.testing import CliRunner

from pin.cli.project import create
from pin.cli.config import init_config
from pin.config import get_config


def get_test_configurations(config_file_path):
    config_contents = dict()
    for path in config_file_path:
        filename = path.split('/')[-1]
        with open(path, 'r') as file:
            config_contents[filename] = file.read()
    return config_contents

def fill_config_folder(folder, contents):
    for filename, content in contents.items():
        with open(f"{folder}/{filename}", "w") as file:
            file.write(content)


def test_init_config():
    # Start a cli runner and execute `pin create test` to
    # generate a new pin project.
    runner = CliRunner()

    config_contents = get_test_configurations(['test_config_files/main_2.yaml',
                                               'test_config_files/main_3.yaml',
                                               'test_config_files/vault.yaml'])

    with runner.isolated_filesystem():
        runner.invoke(create, ['test'])
        os.chdir('test')

        # reset config contents
        shutil.rmtree('config')
        os.mkdir('config')
        fill_config_folder('config', config_contents)
        assert os.listdir('config') == ['main_2.yaml', 'main_3.yaml', 'vault.yaml']

        # The file specific.yaml is missing in the main_2.yaml file
        with pytest.raises(FileNotFoundError):
            get_config('config/main_2.yaml')

        # The entry key2 is missing in vault.yaml
        with pytest.raises(ValueError):
            get_config('config/main_3.yaml')

        # Start init config. This should create
        # The missing file and the missing keys.
        runner.invoke(init_config, input="Y\n value1\n value2")
        assert os.path.isfile('config/specific.yaml')
        config_2 = get_config('config/main_2.yaml')
        config_3 = get_config('config/main_3.yaml')
        assert config_2.test_missing_key == "value1"
        assert config_3.test_missing_key == "value2"

