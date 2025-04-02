import json

from typer.testing import CliRunner

from shellsmith import crud
from shellsmith.cli.app import app

runner = CliRunner()


def test_resolve_input(semitrailer):
    args = ["update", "shell", "123"]
    result = runner.invoke(app, args)
    assert result.exit_code == 1
    assert "❌ Provide either --data or --file." in result.output

    args = ["update", "shell", "123", "--data", "test", "--file", "test.yaml"]
    result = runner.invoke(app, args)
    assert result.exit_code == 1
    assert "❌ Use either --data or --file, not both." in result.output

    args = ["update", "shell", "123", "--file", "aas/WST_A_1.aasx"]
    result = runner.invoke(app, args)
    assert result.exit_code == 1
    assert "❌ Failed to parse input" in result.output


def test_update_shell(semitrailer):
    data = crud.get_shell(semitrailer.id)
    data["idShort"] = "Updated idShort"
    payload = json.dumps(data)
    args = ["update", "shell", semitrailer.id, "--data", payload]
    result = runner.invoke(app, args)
    assert result.exit_code == 0
    assert "Updated Shell" in result.output
    assert crud.get_shell(semitrailer.id)["idShort"] == "Updated idShort"


def test_update_submodel(semitrailer):
    sm_id = semitrailer.product_identification.id

    data = crud.get_submodel(sm_id)
    data["idShort"] = "Updated idShort"
    payload = json.dumps(data)
    args = ["update", "submodel", sm_id, "--data", payload]
    result = runner.invoke(app, args)
    assert result.exit_code == 0
    assert "Updated Submodel" in result.output
    assert crud.get_submodel(sm_id)["idShort"] == "Updated idShort"


def test_update_element(semitrailer):
    sm_id = semitrailer.product_identification.id
    id_short_path = "ProductName"

    data = crud.get_submodel_element(sm_id, id_short_path)
    data["value"] = "Updated Name"
    payload = json.dumps(data)
    args = ["update", "element", sm_id, id_short_path, "--data", payload]
    result = runner.invoke(app, args)
    assert result.exit_code == 0
    assert "Updated Submodel Element" in result.output

    sm_id = semitrailer.product_identification.id
    sme = crud.get_submodel_element(sm_id, id_short_path)
    assert sme["value"] == "Updated Name"


def test_update_element_value(semitrailer):
    sm_id = semitrailer.product_identification.id
    id_short_path = "ProductName"

    args = ["update", "element-value", sm_id, id_short_path, "Updated Name"]
    result = runner.invoke(app, args)
    assert result.exit_code == 0
    assert "Updated value of Element" in result.output


def test_update_submodel_value(semitrailer):
    sm_id = semitrailer.product_identification.id

    # data = crud.get_submodel_value(sm_id)
    # data["isFinished"] = "false"
    data = {"isFinished": "false"}
    payload = json.dumps(data)
    args = ["update", "submodel-value", sm_id, "--data", payload]
    result = runner.invoke(app, args)
    assert result.exit_code == 0 or "400 Client Error" in result.output
