from typer.testing import CliRunner

from shellsmith import crud
from shellsmith.cli.app import app

runner = CliRunner()


def test_cli_nuke():
    runner.invoke(app, ["upload", "aas"])
    assert len(crud.get_shells()) > 0
    assert len(crud.get_submodels()) > 0

    result = runner.invoke(app, ["nuke"], input="n\n")
    assert result.exit_code == 0
    assert "❎ Aborted. No data was deleted." in result.output

    result = runner.invoke(app, ["nuke"], input="y\n")
    assert result.exit_code == 0
    assert "✅ Deleted Shell" in result.output
    assert "✅ Deleted Submodel" in result.output
    assert "🎉 All Shells and Submodels have been deleted." in result.output
    assert len(crud.get_shells()) == 0
    assert len(crud.get_submodels()) == 0

    result = runner.invoke(app, ["nuke"], input="y\n")
    assert result.exit_code == 0
    output = result.output
    assert "✅ Nothing to delete. The AAS environment is already empty." in output
