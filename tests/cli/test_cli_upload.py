from typer.testing import CliRunner

import shellsmith
from shellsmith.cli.app import app

runner = CliRunner()


def test_cli_upload():
    result = runner.invoke(app, ["upload", "aas"])
    assert result.exit_code == 0
    assert "Uploading all" in result.output
    assert len(shellsmith.get_shells()) > 0
    assert len(shellsmith.get_submodels()) > 0

    result = runner.invoke(app, ["upload", "aas/Semitrailer.json"])
    assert "Uploading file" in result.output
    assert result.exit_code == 0

    result = runner.invoke(app, ["upload", "aas/a_typo.json"])
    assert "does not exist or is invalid." in result.output
    assert result.exit_code == 1
