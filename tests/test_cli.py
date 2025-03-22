from pathlib import Path

import shellsmith
from shellsmith.cli import commands


def test_cli_nuke(capsys):
    commands.nuke()
    assert len(shellsmith.get_shells()) == 0
    assert len(shellsmith.get_submodels()) == 0

    commands.info()  # Smoke test
    captured = capsys.readouterr()
    assert "Unreferenced Submodels" not in captured.out
    assert "not found" not in captured.out


def test_cli_upload(capsys, semitrailer):
    commands.upload(Path("aas"))
    assert len(shellsmith.get_shells()) == 2
    assert len(shellsmith.get_submodels()) == 4

    commands.info()  # Smoke test
    captured = capsys.readouterr()
    assert "Unreferenced Submodels" not in captured.out
    assert "not found" not in captured.out

    commands.upload(Path("aas"))
    captured = capsys.readouterr()
    assert "Failed to upload 'Semitrailer.json'" in captured.out
    assert "Failed to upload 'WST_A_1.aasx'" in captured.out

    commands.shell_delete(semitrailer.id, cascade=True)
    commands.upload(Path("aas"))
    captured = capsys.readouterr()
    assert "Failed to upload 'Semitrailer.json'" not in captured.out
    assert "Failed to upload 'WST_A_1.aasx'" in captured.out

    commands.shell_delete(semitrailer.id, cascade=True)
    commands.upload(Path("aas") / "Semitrailer.json")
    captured = capsys.readouterr()
    assert "Failed to upload 'Semitrailer.json'" not in captured.out

    commands.upload(Path("aas") / "Fake.json")
    captured = capsys.readouterr()
    assert "Path 'Fake.json' does not exist or is invalid" not in captured.out
    commands.nuke()


def test_cli_shell_delete(semitrailer, workpiece_carrier_a1, capsys):
    commands.upload(Path("aas"))

    commands.shell_delete(semitrailer.id)
    assert len(shellsmith.get_shells()) == 1
    assert len(shellsmith.get_submodels()) == 4

    commands.info()  # Smoke test
    captured = capsys.readouterr()
    assert "Unreferenced Submodels" in captured.out
    assert "not found" not in captured.out

    commands.shell_delete(semitrailer.id)
    assert len(shellsmith.get_shells()) == 1
    assert len(shellsmith.get_submodels()) == 4
    captured = capsys.readouterr()
    assert f"Failed to delete Shell '{semitrailer.id}" in captured.out

    commands.shell_delete(workpiece_carrier_a1.id, cascade=True)
    assert len(shellsmith.get_shells()) == 0
    assert len(shellsmith.get_submodels()) == 2

    commands.info()  # Smoke test
    captured = capsys.readouterr()
    assert "Unreferenced Submodels" in captured.out
    assert "not found" not in captured.out

    commands.nuke()


def test_cli_submodel_delete(semitrailer, workpiece_carrier_a1, capsys):
    commands.upload(Path("aas"))

    commands.submodel_delete(semitrailer.product_identification.id)
    assert len(shellsmith.get_shells()) == 2
    assert len(shellsmith.get_submodels()) == 3
    submodel_refs = shellsmith.get_submodel_refs(semitrailer.id)
    assert len(submodel_refs) == 2, "Submodel ref should not be removed"

    commands.info()  # Smoke test
    expected = f"Submodel '{semitrailer.product_identification.id}' not found"
    captured = capsys.readouterr()
    assert expected in captured.out

    commands.submodel_delete(semitrailer.product_identification.id)
    expected = f"Submodel '{semitrailer.product_identification.id}' doesn't exist"
    captured = capsys.readouterr()
    assert expected in captured.out

    commands.submodel_delete(semitrailer.production_plan.id, unlink=True)
    assert len(shellsmith.get_shells()) == 2
    assert len(shellsmith.get_submodels()) == 2
    submodel_refs = shellsmith.get_submodel_refs(semitrailer.id)
    assert len(submodel_refs) == 1

    commands.info()  # Smoke test
    expected = f"Submodel '{semitrailer.production_plan.id}' not found"
    captured = capsys.readouterr()
    assert expected not in captured.out

    commands.nuke()
