import os

from click.testing import CliRunner
from pin.cli.project import create
from pin.cli.utils import load_template


def test_create_project_and_overwrite():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(create, ["test"])
        assert not result.exception
        assert result.exit_code == 0

        files_to_check = ["setup.py", "test", "scripts", "config"]
        for file in files_to_check:
            assert file in os.listdir("test")

        # 2nd attempt: no overwriting
        result_2 = runner.invoke(create, ["test"], input="N")
        assert not result.exception
        assert result_2.exit_code == 0
        assert "Aborted" in result_2.output

        # 3rd attempt: overwriting
        result_3 = runner.invoke(create, ["test"], input="Y")
        assert not result.exception
        assert result_3.exit_code == 0
        assert "Aborted" not in result_3.output


def test_create_project_with_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        version = "2.1.0"
        runner.invoke(create, ["test", "--version", version])
        with open("test/setup.py", "r") as setup_file:
            setup_file_content = setup_file.read()
        assert setup_file_content == load_template("setup.tpl", NAME="test", VERSION=version)
