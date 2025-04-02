from shellsmith import crud
from shellsmith.cli.simplify import simplify, simplify_many


def test_simplify(workpiece_carrier_a1):
    shell = crud.get_shell(workpiece_carrier_a1.id)
    simply_shell = simplify(shell)
    assert simply_shell.keys() == {workpiece_carrier_a1.id_short, "submodels"}
    assert simply_shell[workpiece_carrier_a1.id_short] == workpiece_carrier_a1.id


def test_simplify_shells():
    shells = crud.get_shells()
    simplified_shells = simplify_many(shells)
    for shell in simplified_shells:
        assert len(shell.keys()) == 2
        assert "submodels" in shell


def test_simplify_submodel(workpiece_carrier_a1):
    submodel = crud.get_submodel(workpiece_carrier_a1.good_information.id)
    simplified_submodel = simplify(submodel)
    assert simplified_submodel.keys() == {
        workpiece_carrier_a1.good_information.id_short
    }
    assert (
        simplified_submodel[workpiece_carrier_a1.good_information.id_short]
        == workpiece_carrier_a1.good_information.id
    )


def test_simplify_submodels():
    submodels = crud.get_submodels()
    simplified_submodels = simplify_many(submodels)
    for submodel in simplified_submodels:
        assert len(submodel.keys()) == 1
