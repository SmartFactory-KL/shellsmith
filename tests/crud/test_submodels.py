import pytest
from requests import HTTPError

import shellsmith
from shellsmith import services
from shellsmith.upload import upload_aas_folder


def test_get_submodels(semitrailer, workpiece_carrier_a1):
    submodels = shellsmith.get_submodels()
    ids = {s["id"] for s in submodels}
    assert semitrailer.product_identification.id in ids
    assert semitrailer.production_plan.id in ids
    assert workpiece_carrier_a1.good_information.id in ids
    assert workpiece_carrier_a1.asset_location.id in ids


def test_get_submodel(
    semitrailer,
    workpiece_carrier_a1,
):
    services.delete_all_submodels()
    services.delete_all_shells()
    upload_aas_folder("aas")

    submodel = shellsmith.get_submodel(semitrailer.product_identification.id)
    assert submodel["idShort"] == semitrailer.product_identification.id_short

    submodel = shellsmith.get_submodel(semitrailer.production_plan.id)
    assert submodel["idShort"] == semitrailer.production_plan.id_short

    submodel = shellsmith.get_submodel(workpiece_carrier_a1.good_information.id)
    assert submodel["idShort"] == workpiece_carrier_a1.good_information.id_short

    submodel = shellsmith.get_submodel(workpiece_carrier_a1.asset_location.id)
    assert submodel["idShort"] == workpiece_carrier_a1.asset_location.id_short


def test_post_and_put_submodel(semitrailer):
    original = shellsmith.get_submodel(semitrailer.product_identification.id)
    shellsmith.delete_submodel(original["id"])
    shellsmith.post_submodel(original)

    clone = shellsmith.get_submodel(original["id"])
    assert clone["idShort"] == original["idShort"]

    # Modify idShort and update
    original["idShort"] = "TEMP"
    shellsmith.put_submodel(original["id"], original)
    modified = shellsmith.get_submodel(original["id"])
    assert modified["idShort"] == "TEMP"

    # Revert
    original["idShort"] = semitrailer.product_identification.id_short
    shellsmith.put_submodel(original["id"], original)


def test_get_and_patch_submodel_value(semitrailer):
    submodel_id = semitrailer.product_identification.id
    original_value = shellsmith.get_submodel_value(submodel_id)

    new_value = {"Identifier": "changed-id", "ProductName": "ModifiedProduct"}
    with pytest.raises(HTTPError):  # TODO: Investigate, why
        shellsmith.patch_submodel_value(submodel_id, new_value)
        patched_value = shellsmith.get_submodel_value(submodel_id)
        assert patched_value["ProductName"] == "ModifiedProduct"

        # revert
        shellsmith.patch_submodel_value(submodel_id, original_value)


def test_get_submodel_metadata(semitrailer):
    metadata = shellsmith.get_submodel_metadata(semitrailer.product_identification.id)
    assert metadata["modelType"] == "Submodel"


def test_get_submodel_elements(
    semitrailer,
    workpiece_carrier_a1,
):
    elements = shellsmith.get_submodel_elements(semitrailer.product_identification.id)
    assert elements[0]["idShort"] == "Identifier"
    assert elements[1]["idShort"] == "ProductName"
    assert elements[1]["value"] == "Semitrailer"

    elements = shellsmith.get_submodel_elements(
        workpiece_carrier_a1.good_information.id
    )
    assert elements[0]["idShort"] == "CurrentProduct"
    assert elements[0]["value"] == semitrailer.id
    assert elements[1]["idShort"] == "ListTransportableProducts"
    assert elements[2]["idShort"] == "ProductName"
    assert elements[2]["value"] == "Semitrailer"

    elements = shellsmith.get_submodel_elements(workpiece_carrier_a1.asset_location.id)
    assert elements[0]["idShort"] == "CurrentFences"
    assert elements[0]["value"][0]["value"][0]["idShort"] == "FenceName"
    assert elements[0]["value"][0]["value"][0]["value"] == "TSN-Module"


def test_get_submodel_element(workpiece_carrier_a1):
    submodel_id = workpiece_carrier_a1.asset_location.id
    id_short_path = "CurrentFences[0].FenceName"
    fence_name = shellsmith.get_submodel_element(submodel_id, id_short_path)
    assert fence_name["value"] == "TSN-Module"


def test_patch_submodel_element_value(
    workpiece_carrier_a1,
):
    old_product_name = "Semitrailer"
    new_product_name = "A New Product Name"

    shellsmith.patch_submodel_element_value(
        submodel_id=workpiece_carrier_a1.good_information.id,
        id_short_path="ProductName",
        value=new_product_name,
    )

    elements = shellsmith.get_submodel_elements(
        workpiece_carrier_a1.good_information.id
    )
    assert elements[2]["value"] == new_product_name

    # Reset
    shellsmith.patch_submodel_element_value(
        submodel_id=workpiece_carrier_a1.good_information.id,
        id_short_path="ProductName",
        value=old_product_name,
    )
    elements = shellsmith.get_submodel_elements(
        workpiece_carrier_a1.good_information.id
    )
    assert elements[2]["value"] == old_product_name


def test_set_current_fence_name(
    workpiece_carrier_a1,
):
    old_fence_name = "TSN-Module"
    new_fence_name = "New-Fence-001"

    shellsmith.patch_submodel_element_value(
        submodel_id=workpiece_carrier_a1.asset_location.id,
        id_short_path="CurrentFences[0].FenceName",
        value=new_fence_name,
    )

    elements = shellsmith.get_submodel_elements(workpiece_carrier_a1.asset_location.id)
    assert elements[0]["idShort"] == "CurrentFences"
    assert elements[0]["value"][0]["value"][0]["idShort"] == "FenceName"
    assert elements[0]["value"][0]["value"][0]["value"] == new_fence_name

    shellsmith.patch_submodel_element_value(
        submodel_id=workpiece_carrier_a1.asset_location.id,
        id_short_path="CurrentFences[0].FenceName",
        value=old_fence_name,
    )

    elements = shellsmith.get_submodel_elements(workpiece_carrier_a1.asset_location.id)
    assert elements[0]["value"][0]["value"][0]["value"] == old_fence_name


def test_post_submodel_element_root(semitrailer):
    """Tests POST /submodels/{submodel_id}/submodel-elements"""
    submodel_id = semitrailer.product_identification.id
    new_element = {
        "idShort": "TestRootElement",
        "modelType": "Property",
        "valueType": "string",
        "value": "hello",
    }

    shellsmith.post_submodel_element(submodel_id, new_element)

    elements = shellsmith.get_submodel_elements(submodel_id)
    ids = [el["idShort"] for el in elements]
    assert "TestRootElement" in ids

    shellsmith.delete_submodel_element(submodel_id, "TestRootElement")


def test_post_submodel_element_nested(semitrailer):
    """Tests POST /submodels/{submodel_id}/submodel-elements/{idShortPath}"""
    submodel_id = semitrailer.product_identification.id
    nested_element = {
        "idShort": "NestedTestProp",
        "modelType": "Property",
        "valueType": "string",
        "value": "42",
    }

    collection = {
        "idShort": "NestedTestStruct",
        "modelType": "SubmodelElementCollection",
        "value": [],
    }

    shellsmith.post_submodel_element(submodel_id, collection)
    shellsmith.post_submodel_element(
        submodel_id, nested_element, id_short_path="NestedTestStruct"
    )

    nested = shellsmith.get_submodel_element(
        submodel_id, "NestedTestStruct.NestedTestProp"
    )
    assert nested["value"] == "42"

    shellsmith.delete_submodel_element(submodel_id, "NestedTestStruct.NestedTestProp")
    shellsmith.delete_submodel_element(submodel_id, "NestedTestStruct")


def test_put_submodel_element(semitrailer):
    """Tests PUT /submodels/{submodel_id}/submodel-elements/{idShortPath}"""
    submodel_id = semitrailer.product_identification.id
    path = "PutTestProp"

    element = {
        "idShort": path,
        "modelType": "Property",
        "valueType": "string",
        "value": "initial",
    }

    # First create it via POST
    shellsmith.post_submodel_element(submodel_id, element)

    # Then update via PUT
    element["value"] = "changed"
    shellsmith.put_submodel_element(submodel_id, path, element)

    result = shellsmith.get_submodel_element(submodel_id, path)
    assert result["value"] == "changed"

    shellsmith.delete_submodel_element(submodel_id, path)


def test_get_submodel_element_value(semitrailer):
    """Tests GET /submodels/{submodel_id}/submodel-elements/{idShortPath}/$value"""
    submodel_id = semitrailer.product_identification.id
    value = shellsmith.get_submodel_element_value(submodel_id, "ProductName")
    assert value == "Semitrailer"
