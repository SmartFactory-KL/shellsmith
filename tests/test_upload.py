import shellsmith
from shellsmith import services
from shellsmith.upload import upload_aas_folder


def test_upload():
    services.delete_all_shells()
    services.delete_all_submodels()
    assert len(shellsmith.get_shells()) == 0
    upload_aas_folder("aas")
    assert len(shellsmith.get_shells()) == 2
    assert len(shellsmith.get_submodels()) == 4
