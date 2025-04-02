import json

from typer.testing import CliRunner

from shellsmith import crud
from shellsmith.cli.app import app
from shellsmith.utils import generate_id

runner = CliRunner()


def test_create_shell():
    payload = {
        "idShort": "TestShell",
        "id": generate_id("shell"),
        "assetInformation": {
            "assetKind": "Instance",
            "globalAssetId": generate_id("asset"),
        },
        "modelType": "AssetAdministrationShell",
    }

    result = runner.invoke(app, ["create", "shell", "--data", json.dumps(payload)])

    assert result.exit_code == 0
    assert "Created Shell" in result.output


def test_create_submodel():
    payload = {
        "idShort": "TestSubmodel",
        "id": generate_id("submodel"),
        "kind": "Instance",
        "modelType": "Submodel",
    }

    result = runner.invoke(
        app,
        [
            "create",
            "submodel",
            "--data",
            json.dumps(payload),
        ],
    )

    assert result.exit_code == 0
    assert "Created Submodel" in result.output


def test_create_submodel_ref(semitrailer):
    ref = {
        "keys": [{"type": "Submodel", "value": generate_id("submodel")}],
        "type": "ExternalReference",
    }

    result = runner.invoke(
        app,
        [
            "create",
            "submodel-ref",
            semitrailer.id,
            "--data",
            json.dumps(ref),
        ],
    )

    assert result.exit_code == 0
    assert "Created Submodel reference" in result.output


def test_create_element_root(semitrailer):
    element = {
        "idShort": "NewElement",
        "modelType": "Property",
        "valueType": "xs:string",
        "value": "42",
    }

    result = runner.invoke(
        app,
        [
            "create",
            "element",
            semitrailer.product_identification.id,
            "--data",
            json.dumps(element),
        ],
    )

    assert result.exit_code == 0
    assert "Created root-level Element" in result.output


def test_create_element_nested(workpiece_carrier_a1):
    submodel_id = workpiece_carrier_a1.asset_location.id

    # Fetch an existing element and repurpose it
    data = crud.get_submodel_element(submodel_id, "CurrentFences[0].FenceName")
    data["idShort"] = "NestedCopy"
    data["value"] = "Hello nested"
    payload = json.dumps(data)

    id_short_path = "CurrentFences[0]"

    result = runner.invoke(
        app,
        [
            "create",
            "element",
            submodel_id,
            id_short_path,
            "--data",
            payload,
        ],
    )
    assert result.exit_code == 0
    assert "Created nested Element" in result.output

    data = crud.get_submodel_element(submodel_id, "CurrentFences[0].NestedCopy")
    assert data["idShort"] == "NestedCopy"
    assert data["value"] == "Hello nested"
