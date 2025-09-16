import pytest
from httpx import HTTPStatusError

import shellsmith


def test_health():
    assert shellsmith.is_healthy()
    assert shellsmith.get_health_status() == "UP"


def test_get_shells(semitrailer, workpiece_carrier_a1):
    shells = shellsmith.get_shells()
    shells = shells["result"]
    ids = [s["id"] for s in shells]
    assert semitrailer.id in ids
    assert workpiece_carrier_a1.id in ids


def test_get_shell(semitrailer):
    shell = shellsmith.get_shell(semitrailer.id)
    assert shell["id"] == semitrailer.id
    assert shell["idShort"] == semitrailer.id_short


def test_post_shell():
    shell_id = "https://example.com/shells/test-post"
    new_shell = {
        "idShort": "TestPostShell",
        "id": shell_id,
        "assetInformation": {
            "assetKind": "Instance",
            "globalAssetId": "https://example.com/assets/test",
        },
        "submodels": [],
        "modelType": "AssetAdministrationShell",
    }
    shellsmith.post_shell(new_shell)
    result = shellsmith.get_shell(shell_id)
    assert result["id"] == shell_id
    shellsmith.delete_shell(shell_id)


def test_put_shell():
    shell_id = "https://example.com/shells/test-put"
    shell = {
        "idShort": "PutShellInitial",
        "id": shell_id,
        "assetInformation": {
            "assetKind": "Instance",
            "globalAssetId": "https://example.com/assets/put",
        },
        "submodels": [],
        "modelType": "AssetAdministrationShell",
    }
    shellsmith.post_shell(shell)
    shell["idShort"] = "PutShellUpdated"
    shellsmith.put_shell(shell_id, shell)
    updated = shellsmith.get_shell(shell_id)
    assert updated["idShort"] == "PutShellUpdated"
    shellsmith.delete_shell(shell_id)


def test_delete_shell():
    shell_id = "https://example.com/shells/test-delete"
    shell = {
        "idShort": "DeleteShell",
        "id": shell_id,
        "assetInformation": {
            "assetKind": "Instance",
            "globalAssetId": "https://example.com/assets/delete",
        },
        "submodels": [],
        "modelType": "AssetAdministrationShell",
    }
    shellsmith.post_shell(shell)
    shellsmith.delete_shell(shell_id)
    with pytest.raises(HTTPStatusError):
        shellsmith.get_shell(shell_id)


def test_post_and_delete_submodel_ref(semitrailer):
    shell_id = semitrailer.id
    test_submodel_id = "https://example.com/submodels/test-submodel"
    submodel_ref = {
        "type": "ModelReference",
        "keys": [
            {
                "type": "Submodel",
                "value": test_submodel_id,
            }
        ],
    }

    shellsmith.post_submodel_ref(shell_id, submodel_ref)
    refs = shellsmith.get_submodel_refs(shell_id)["result"]
    assert any(ref["keys"][0]["value"] == test_submodel_id for ref in refs)

    shellsmith.delete_submodel_ref(shell_id, test_submodel_id)
    refs = shellsmith.get_submodel_refs(shell_id)["result"]
    assert all(ref["keys"][0]["value"] != test_submodel_id for ref in refs)
