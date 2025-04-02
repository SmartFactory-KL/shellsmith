from typer.testing import CliRunner

from shellsmith.cli.app import app

runner = CliRunner()


def test_cli_decode():
    result = runner.invoke(app, ["decode", "dGVzdA=="])
    assert result.exit_code == 0
    assert "test" in result.output.strip()
