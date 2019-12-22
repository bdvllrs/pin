from pin.config import get_config


def test_get_config():
    config = get_config('test_cli/test_config_files/main.yaml')

    assert config.test == "value1"
    assert config.test2.item == "value"
