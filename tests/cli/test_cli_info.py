from typer.testing import CliRunner

from shellsmith import crud
from shellsmith.cli.app import app

runner = CliRunner()


def test_cli_info(semitrailer, workpiece_carrier_a1):
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "shellsmith - AAS Toolkit" in result.output
    assert "Semitrailer" in result.output

    crud.delete_submodel(semitrailer.product_identification.id)
    crud.delete_shell(workpiece_carrier_a1.id)
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "⚠️ Unreferenced Submodel" in result.output
    assert "⚠️ Dangling Submodel References" in result.output
