import shellsmith
from shellsmith import services
from shellsmith.upload import upload_aas_folder


def test_upload():
    services.delete_all_shells()
    services.delete_all_submodels()
    shells = shellsmith.get_shells()["result"]
    assert len(shells) == 0
    upload_aas_folder("aas")
    shells = shellsmith.get_shells()["result"]
    submodels = shellsmith.get_submodels()["result"]
    assert len(shells) == 2
    assert len(submodels) == 4
