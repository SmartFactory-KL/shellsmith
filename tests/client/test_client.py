import pytest

from shellsmith.clients import Client


def test_sync_client_smoke():
    with Client(host="http://localhost:8099", timeout=0.01) as client:
        assert client.get_health_status() == "DOWN"
        assert client.is_healthy() is False

    with Client() as client:
        # Health
        assert client.get_health_status() == "UP"
        assert client.is_healthy() is True

        # Get
        shells = client.get_shells()
        assert len(shells["result"]) == 2
        submodels = client.get_submodels()
        assert len(submodels["result"]) == 4

        # POST
        test_shell = {
            "id": "test-shell-id",
            "idShort": "TestShell",
            "modelType": "AssetAdministrationShell",
        }
        test_submodel = {
            "id": "test-submodel-id",
            "idShort": "TestSubmodel",
            "modelType": "Submodel",
        }

        created_shell = client.create_shell(test_shell)
        assert created_shell["id"] == "test-shell-id"
        shells = client.get_shells()
        assert len(shells["result"]) == 3

        created_submodel = client.create_submodel(test_submodel)
        assert created_submodel["id"] == "test-submodel-id"
        submodels = client.get_submodels()
        assert len(submodels["result"]) == 5

        assert client.get_shell("test-shell-id")["id"] == "test-shell-id"
        assert client.get_submodel("test-submodel-id")["id"] == "test-submodel-id"

        # PUT Shell
        client.update_shell(
            "test-shell-id",
            {**test_shell, "idShort": "UpdatedTestShell"},
        )

        # PUT Submodel
        client.update_submodel(
            "test-submodel-id",
            {**test_submodel, "idShort": "UpdatedTestSubmodel"},
        )

        # GET $value
        assert client.get_submodel_value("test-submodel-id") == {}
        test_element = {
            "idShort": "testElement",
            "modelType": "Property",
            "valueType": "xs:string",
            "value": "testValue",
        }

        # POST Submodel-Element
        client.create_submodel_element("test-submodel-id", test_element)
        elements = client.get_submodel_elements("test-submodel-id")
        assert len(elements["result"]) == 1

        # GET Submodel-Element $value
        element_value = client.get_submodel_element_value(
            "test-submodel-id",
            "testElement",
        )
        assert element_value == "testValue"

        # PATCH Submodel $value
        payload = [
            {
                "modelType": "Property",
                "idShort": "testElement",
                "valueType": "xs:string",
                "value": "viaSubmodelPatch",
            }
        ]
        client.update_submodel_value("test-submodel-id", payload)
        value = client.get_submodel_element_value("test-submodel-id", "testElement")
        assert value == "viaSubmodelPatch"

        # PATCH Submodel-Element $value
        client.update_submodel_element_value(
            "test-submodel-id", "testElement", "viaElementPatch"
        )
        value = client.get_submodel_element_value("test-submodel-id", "testElement")
        assert value == "viaElementPatch"

        # PUT Submodel-Element
        client.update_submodel_element(
            "test-submodel-id",
            "testElement",
            {**test_element, "value": "updatedValue"},
        )
        value = client.get_submodel_element_value("test-submodel-id", "testElement")
        assert value == "updatedValue"

        # Submodel Metadata
        assert client.get_submodel_metadata("test-submodel-id")

        # Submodel Refs
        assert len(client.get_submodel_refs("test-shell-id")["result"]) == 0
        client.create_submodel_ref(
            "test-shell-id",
            {"keys": [{"type": "Submodel", "value": "test-submodel-id"}]},
        )
        assert len(client.get_submodel_refs("test-shell-id")["result"]) == 1

        # Cleanup
        client.delete_submodel_element("test-submodel-id", "testElement")
        client.delete_submodel_ref("test-shell-id", "test-submodel-id")
        client.delete_shell("test-shell-id")
        client.delete_submodel("test-submodel-id")

        # Upload
        client.upload_aas_folder("aas")
        with pytest.raises(ValueError):
            client.upload_aas_folder("aas-i-dont-exist")

    with pytest.raises(RuntimeError):
        client.get_shells()
