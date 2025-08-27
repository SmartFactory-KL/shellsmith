from typer.testing import CliRunner

from shellsmith import api
from shellsmith.cli.app import app

runner = CliRunner()


def test_cli_upload():
    result = runner.invoke(app, ["upload", "aas"])
    assert result.exit_code == 0
    assert "Uploading all" in result.output
    assert len(api.get_shells()["result"]) > 0
    assert len(api.get_submodels()["result"]) > 0

    result = runner.invoke(app, ["upload", "aas/Semitrailer.json"])
    assert "Uploading file" in result.output
    assert result.exit_code == 0

    result = runner.invoke(app, ["upload", "aas/a_typo.json"])
    assert "does not exist or is invalid." in result.output
    assert result.exit_code == 1
