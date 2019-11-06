import inspect
from pin.sacred import munchify


@munchify
def fake_main(_run, _config, param=1):
    pass


def test_munchify():
    assert str(inspect.signature(fake_main)) == "(_run, _config, param=1)"
