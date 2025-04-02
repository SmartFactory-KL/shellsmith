from typer.testing import CliRunner

from shellsmith.cli.app import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "shellsmith - AAS Toolkit command-line interface." in result.output
