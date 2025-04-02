from typer.testing import CliRunner

from shellsmith.cli.app import app

runner = CliRunner()


def test_delete_submodel_ref(semitrailer):
    result = runner.invoke(
        app,
        [
            "delete",
            "submodel-ref",
            semitrailer.id,
            semitrailer.production_plan.id,
        ],
    )
    assert result.exit_code == 0
    assert "Deleted Submodel reference" in result.output


def test_delete_element(semitrailer):
    result = runner.invoke(
        app,
        [
            "delete",
            "element",
            semitrailer.product_identification.id,
            "ProductName",
        ],
    )
    assert result.exit_code == 0
    assert "Deleted Element" in result.output


def test_delete_submodel_without_refs(semitrailer):
    result = runner.invoke(
        app,
        [
            "delete",
            "submodel",
            semitrailer.product_identification.id,
        ],
    )
    assert result.exit_code == 0
    assert "Deleted Submodel" in result.output


def test_delete_submodel_with_refs(workpiece_carrier_a1):
    result = runner.invoke(
        app,
        [
            "delete",
            "submodel",
            workpiece_carrier_a1.asset_location.id,
            "--remove-refs",
        ],
    )
    assert result.exit_code == 0
    assert "Deleted Submodel" in result.output
    assert "Removed reference" in result.output


def test_delete_shell_only(semitrailer):
    result = runner.invoke(app, ["delete", "shell", semitrailer.id])
    assert result.exit_code == 0
    assert "Deleted Shell" in result.output


def test_delete_shell_with_cascade(workpiece_carrier_a1):
    result = runner.invoke(
        app, ["delete", "shell", workpiece_carrier_a1.id, "--cascade"]
    )
    assert result.exit_code == 0
    assert "Deleted referenced Submodel" in result.output
    assert "Deleted Shell" in result.output
