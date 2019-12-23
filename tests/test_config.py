from pin.config import load_config


def test_load_config():
    conf = load_config('test_cli/test_config_files/main.yaml')

    assert conf.test == "value1"
    assert conf.test2.item == "value"
