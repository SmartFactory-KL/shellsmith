"""Deletes all shells and submodels from the AAS environment."""

from shellsmith import services


def nuke() -> None:
    """Deletes all AAS Shells and Submodels.

    Calls both Shell and Submodel deletion routines.
    """
    print("☣️ Deleting all Shells and Submodels!")
    print("☢️ Deleting all Shells and Submodels!")
    print("⚠️ Deleting all Shells and Submodels!")
    services.delete_all_shells()
    services.delete_all_submodels()
