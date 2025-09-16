import pytest

from shellsmith.clients import AsyncClient


@pytest.mark.asyncio
async def test_async_client_smoke():
    async with AsyncClient(host="http://localhost:8099", timeout=0.01) as client:
        assert await client.get_health_status() == "DOWN"
        assert await client.is_healthy() is False

    async with AsyncClient() as client:
        # Health
        assert await client.get_health_status() == "UP"
        assert await client.is_healthy() is True

        # GET
        shells = await client.get_shells()
        assert len(shells["result"]) == 2
        submodels = await client.get_submodels()
        assert len(submodels["result"]) == 4

        # POST
        test_shell = {
            "id": "test-async-shell-id",
            "idShort": "TestAsyncShell",
            "modelType": "AssetAdministrationShell",
        }
        test_submodel = {
            "id": "test-async-submodel-id",
            "idShort": "TestAsyncSubmodel",
            "modelType": "Submodel",
        }

        created_shell = await client.create_shell(test_shell)
        assert created_shell["id"] == "test-async-shell-id"
        shells = await client.get_shells()
        assert len(shells["result"]) == 3

        created_submodel = await client.create_submodel(test_submodel)
        assert created_submodel["id"] == "test-async-submodel-id"
        submodels = await client.get_submodels()
        assert len(submodels["result"]) == 5

        shell = await client.get_shell("test-async-shell-id")
        assert shell["id"] == "test-async-shell-id"

        submodel = await client.get_submodel("test-async-submodel-id")
        assert submodel["id"] == "test-async-submodel-id"

        # PUT Shell
        await client.update_shell(
            "test-async-shell-id", {**test_shell, "idShort": "UpdatedTestAsyncShell"}
        )

        # PUT Submodel
        await client.update_submodel(
            "test-async-submodel-id",
            {**test_submodel, "idShort": "UpdatedTestAsyncSubmodel"},
        )

        # GET $value
        assert await client.get_submodel_value("test-async-submodel-id") == {}
        test_element = {
            "idShort": "testElement",
            "modelType": "Property",
            "valueType": "xs:string",
            "value": "testValue",
        }

        # POST Submodel-Element
        await client.create_submodel_element("test-async-submodel-id", test_element)
        elements = await client.get_submodel_elements("test-async-submodel-id")
        assert len(elements["result"]) == 1

        # GET Submodel-Element
        element = await client.get_submodel_element(
            "test-async-submodel-id",
            "testElement",
        )
        assert element["idShort"] == "testElement"

        # GET Submodel-Element $value
        element_value = await client.get_submodel_element_value(
            "test-async-submodel-id",
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
        await client.update_submodel_value("test-async-submodel-id", payload)
        element_value = await client.get_submodel_element_value(
            "test-async-submodel-id",
            "testElement",
        )
        assert element_value == "viaSubmodelPatch"

        # PATCH Submodel-Element $value
        await client.update_submodel_element_value(
            "test-async-submodel-id",
            "testElement",
            "viaElementPatch",
        )
        element_value = await client.get_submodel_element_value(
            "test-async-submodel-id",
            "testElement",
        )
        assert element_value == "viaElementPatch"

        # PUT Submodel-Element
        test_element["value"] = "updatedValue"
        await client.update_submodel_element(
            "test-async-submodel-id",
            "testElement",
            test_element,
        )
        element_value = await client.get_submodel_element_value(
            "test-async-submodel-id",
            "testElement",
        )
        assert element_value == "updatedValue"

        # Submodel Metadata
        assert await client.get_submodel_metadata("test-async-submodel-id")

        # Submodel Refs
        submodel_refs = await client.get_submodel_refs("test-async-shell-id")
        assert len(submodel_refs["result"]) == 0
        test_ref = {"keys": [{"type": "Submodel", "value": "test-async-submodel-id"}]}
        await client.create_submodel_ref("test-async-shell-id", test_ref)
        submodel_refs = await client.get_submodel_refs("test-async-shell-id")
        assert len(submodel_refs["result"]) == 1

        # Cleanup
        await client.delete_submodel_element("test-async-submodel-id", "testElement")
        await client.delete_submodel_ref(
            "test-async-shell-id", "test-async-submodel-id"
        )
        await client.delete_shell("test-async-shell-id")
        await client.delete_submodel("test-async-submodel-id")

        # Upload
        shells = await client.get_shells()
        shell_id = shells["result"][0]["id"]
        submodel_ids = [
            sm["keys"][0]["value"] for sm in shells["result"][0]["submodels"]
        ]
        for submodel_id in submodel_ids:
            await client.delete_submodel(submodel_id)
        await client.delete_shell(shell_id)
        await client.upload_aas_folder("aas")
        with pytest.raises(ValueError):
            await client.upload_aas_folder("aas-i-dont-exist")

    with pytest.raises(RuntimeError):
        await client.get_shells()
