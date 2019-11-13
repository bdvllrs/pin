import os
from pathlib import Path
from click.testing import CliRunner
from pin.cli.utils import PROJECT_DIR
from pin.cli.project import create
from pin.cli.scripts import add_script, list_templates


def test_add_script():
    runner = CliRunner()
    with runner.isolated_filesystem():
        runner.invoke(create, ["test"])
        os.chdir("test")
        assert "scripts" in os.listdir(".")
        result = runner.invoke(add_script, ["test"])
        assert not result.exception
        assert result.exit_code == 0
        new_script = Path("scripts/test.py")
        assert new_script.exists()


def test_list_template():
    runner = CliRunner()
    with runner.isolated_filesystem():
        runner.invoke(create, ["test"])
        os.chdir("test")
        result = runner.invoke(list_templates)
        assert not result.exception
        output = result.output[1:-2].split("\n-")
        assert len(output) == len(os.listdir(PROJECT_DIR / "templates/scripts"))
