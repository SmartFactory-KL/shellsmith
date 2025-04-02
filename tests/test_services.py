import pytest
from requests import HTTPError

import shellsmith
from shellsmith import services


def test_get_shell_submodels(semitrailer):
    submodels = services.get_shell_submodels(semitrailer.id)
    ids = {s["id"] for s in submodels}
    assert semitrailer.product_identification.id in ids
    assert semitrailer.production_plan.id in ids


def test_delete_shell_cascading(semitrailer):
    shell_id = semitrailer.id
    services.delete_shell_cascading(shell_id)
    with pytest.raises(HTTPError):
        shellsmith.get_shell(shell_id)


def test_remove_submodel_references(semitrailer):
    submodel_id = semitrailer.product_identification.id
    services.remove_submodel_references(submodel_id)
    for shell in shellsmith.get_shells():
        assert submodel_id not in {
            ref["keys"][0]["value"] for ref in shell.get("submodels", [])
        }


def test_find_unreferenced_submodels(semitrailer):
    services.delete_all_submodels()
    services.delete_all_shells()
    shellsmith.upload_aas_folder("aas")
    services.remove_submodel_references(semitrailer.product_identification.id)
    unreferenced = services.find_unreferenced_submodels()
    assert semitrailer.product_identification.id in unreferenced


def test_find_dangling_submodel_refs(semitrailer):
    submodel_id = semitrailer.production_plan.id
    assert not services.find_dangling_submodel_refs()
    shellsmith.delete_submodel(submodel_id)
    dangling = services.find_dangling_submodel_refs()
    dangling_submodel = dangling[0]["submodels"][0]
    assert dangling_submodel["<missing>"] == submodel_id


def test_remove_dangling_submodel_refs():
    assert services.find_dangling_submodel_refs()
    services.remove_dangling_submodel_refs()
    assert not services.find_dangling_submodel_refs()


def test_health_down():
    assert services.health(host="https://example.com") == "DOWN"


def test_delete_submodels_of_shell(semitrailer):
    services.delete_all_submodels()
    services.delete_all_shells()
    shellsmith.upload_aas_folder("aas")
    shellsmith.delete_submodel(semitrailer.product_identification.id)
    services.delete_submodels_of_shell(semitrailer.id)
    assert not services.find_unreferenced_submodels()
