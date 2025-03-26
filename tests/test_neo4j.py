import os
import time

import pytest

if not os.getenv("SHELLSMITH_NEO4J_ENABLED"):
    pytest.skip(
        reason="Skipping Neo4j tests. Set SHELLSMITH_NEO4J_ENABLED=1 to enable.",
        allow_module_level=True,
    )

from shellsmith import neo4j, services
from shellsmith.upload import upload_aas_folder

GRAPH_READY_TIMEOUT = 45  # seconds
EXPECTED_NODE_COUNT = 39
EXPECTED_SUBMODEL_ELEMENT_COUNT = 17  # or whatever your total is


def wait_for_graph_node_count(
    expected_count: int = EXPECTED_NODE_COUNT,
    timeout: int = GRAPH_READY_TIMEOUT,
) -> (bool, int):
    query = "MATCH (n) RETURN count(n) AS count"
    start = time.time()

    last_count = 0

    while True:
        try:
            with neo4j.get_driver().session() as session:
                result = session.run(query)
                record = result.single()
                count = record["count"]
                last_count = count
                if record and count == expected_count:
                    return True, last_count
        except Exception:  # noqa
            pass  # wait and retry

        if time.time() - start > timeout:
            return False, last_count

        time.sleep(0.5)


def test_wait_for_graph():
    # neo4j.detach_delete_all()
    services.delete_all_shells()
    services.delete_all_submodels()
    success, count = wait_for_graph_node_count(0)
    assert success, f"Graph was not fully destructed within timeout: {count}"

    upload_aas_folder("aas")
    success, count = wait_for_graph_node_count(39)
    assert success, f"Graph was not fully built within timeout: {count}"
    time.sleep(1)


def test_get_shells(semitrailer, workpiece_carrier_a1):
    shells = neo4j.get_shells()
    assert len(shells) == 2

    shell_id_shorts = {shell["idShort"] for shell in shells}
    shell_ids = {shell["id"] for shell in shells}
    assert semitrailer.id in shell_ids
    assert workpiece_carrier_a1.id in shell_ids
    assert semitrailer.id_short in shell_id_shorts
    assert workpiece_carrier_a1.id_short in shell_id_shorts


def test_get_shell(
    semitrailer,
    workpiece_carrier_a1,
):
    shell = neo4j.get_shell(semitrailer.id)
    assert shell["id"] == semitrailer.id
    assert shell["idShort"] == semitrailer.id_short

    shell = neo4j.get_shell(workpiece_carrier_a1.id)
    assert shell["id"] == workpiece_carrier_a1.id
    assert shell["idShort"] == workpiece_carrier_a1.id_short


def test_get_submodels(semitrailer, workpiece_carrier_a1):
    submodels = neo4j.get_submodels()
    assert len(submodels) == 4


def test_get_submodel(
    semitrailer,
    workpiece_carrier_a1,
):
    submodel = neo4j.get_submodel(semitrailer.product_identification.id)
    assert submodel["idShort"] == semitrailer.product_identification.id_short

    submodel = neo4j.get_submodel(semitrailer.production_plan.id)
    assert submodel["idShort"] == semitrailer.production_plan.id_short

    submodel = neo4j.get_submodel(workpiece_carrier_a1.good_information.id)
    assert submodel["idShort"] == workpiece_carrier_a1.good_information.id_short

    submodel = neo4j.get_submodel(workpiece_carrier_a1.asset_location.id)
    assert submodel["idShort"] == workpiece_carrier_a1.asset_location.id_short


def test_get_submodel_elements(semitrailer, workpiece_carrier_a1):
    elements = neo4j.get_submodel_elements(semitrailer.product_identification.id)
    assert len(elements) == 2
    id_shorts = {el["idShort"] for el in elements}
    assert "Identifier" in id_shorts
    assert "ProductName" in id_shorts

    elements = neo4j.get_submodel_elements(workpiece_carrier_a1.good_information.id)
    assert len(elements) == 7
    id_shorts = {el["idShort"] for el in elements}
    assert "CurrentProduct" in id_shorts
    assert "ListTransportableProducts" in id_shorts
    assert "ProductName" in id_shorts


def test_get_submodel_element(semitrailer, workpiece_carrier_a1):
    element = neo4j.get_submodel_element(
        semitrailer.product_identification.id, "ProductName"
    )
    assert element["idShort"] == "ProductName"
    assert element["value"] == "Semitrailer"

    element = neo4j.get_submodel_element(
        workpiece_carrier_a1.asset_location.id, "CurrentFences[0].FenceName"
    )
    assert element["idShort"] == "FenceName"
    assert element["value"] == "TSN-Module"


def test_close_driver():
    neo4j.close_driver()
