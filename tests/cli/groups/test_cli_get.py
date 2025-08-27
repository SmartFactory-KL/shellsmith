from typer.testing import CliRunner

from shellsmith.cli.app import app

runner = CliRunner()


def test_get_shells():
    result = runner.invoke(app, ["get", "shells"])
    assert result.exit_code == 0
    assert "Semitrailer" in result.output


def test_get_shells_with_incorrect_host():
    result = runner.invoke(app, ["get", "shells", "--host", "https://example.com"])
    assert result.exit_code == 1
    assert "Client error '404 Not Found" in result.output


def test_get_shell(semitrailer):
    args = ["get", "shell", semitrailer.id, "--output", "yaml"]
    result = runner.invoke(app, args)
    assert result.exit_code == 0
    assert semitrailer.id_short in result.output


def test_get_shell_not_found():
    result = runner.invoke(app, ["get", "shell", "123"])
    assert result.exit_code == 1
    assert "404" in result.output
    assert "Client error" in result.output


def test_get_submodel_refs(semitrailer):
    result = runner.invoke(app, ["get", "submodel-refs", semitrailer.id])
    assert result.exit_code == 0
    assert semitrailer.product_identification.id in result.output


def test_get_submodels():
    result = runner.invoke(app, ["get", "submodels"])
    assert result.exit_code == 0
    assert "ProductIdentification" in result.output


def test_get_submodel(semitrailer):
    result = runner.invoke(
        app, ["get", "submodel", semitrailer.product_identification.id]
    )
    assert result.exit_code == 0
    assert "ProductIdentification" in result.output


def test_get_submodel_value(semitrailer):
    result = runner.invoke(
        app, ["get", "submodel-value", semitrailer.product_identification.id]
    )
    assert result.exit_code == 0


def test_get_submodel_meta(semitrailer):
    result = runner.invoke(
        app, ["get", "submodel-meta", semitrailer.product_identification.id]
    )
    assert result.exit_code == 0


def test_get_elements(semitrailer):
    result = runner.invoke(
        app, ["get", "elements", semitrailer.product_identification.id]
    )
    assert result.exit_code == 0
    assert "idShort" in result.output


def test_get_element(semitrailer):
    result = runner.invoke(
        app, ["get", "element", semitrailer.product_identification.id, "ProductName"]
    )
    assert result.exit_code == 0
    assert "idShort: ProductName" in result.output


def test_get_element_value(semitrailer):
    result = runner.invoke(
        app,
        ["get", "element-value", semitrailer.product_identification.id, "ProductName"],
    )
    assert result.exit_code == 0
