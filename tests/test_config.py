import os

from pin.cli.utils import PROJECT_DIR
from pin.config import load_config, update_argv_from_arguments


def test_load_config():
    conf = load_config(os.path.join(PROJECT_DIR.parent,
                                    'tests/test_cli/test_config_files/main.yaml'))

    assert conf.test == "value1"
    assert conf.test2.item == "value"


def test_update_from_arguments():
    path = os.path.join(PROJECT_DIR.parent,
                        'tests/test_cli/test_config_files/main.yaml')
    conf = load_config(path)
    args = ["python main.py", "with", "'test=@{vault:key2}'", "test2=3"]
    update_argv_from_arguments(args, conf, path)
    assert args[2] == "'test=value2'"
    assert args[3] == "'test2=3'"
