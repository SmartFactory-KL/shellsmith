from shellsmith import crud, services
from shellsmith.upload import upload_aas_folder


def test_upload():
    services.delete_all_shells()
    services.delete_all_submodels()
    assert len(crud.get_shells()) == 0
    upload_aas_folder("aas")
    assert len(crud.get_shells()) == 2
    assert len(crud.get_submodels()) == 4
