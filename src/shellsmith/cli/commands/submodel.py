"""Handles deletion of submodels and their Shell references."""

import requests

import shellsmith
from shellsmith import services


def submodel_delete(submodel_id: str, unlink: bool = False) -> None:
    """Deletes a Submodel by its ID, optionally removing all Shell references.

    Args:
        submodel_id: The unique identifier of the Submodel to delete.
        unlink: If True, removes all references to the Submodel from existing Shells.
    """
    print(f"🗑️ Deleting Submodel: {submodel_id}")
    try:
        shellsmith.delete_submodel(submodel_id)
        print(f"✅ Submodel '{submodel_id}' deleted.")
    except requests.exceptions.HTTPError:
        print(f"❌ Submodel '{submodel_id}' doesn't exist.")
    if unlink:
        services.remove_submodel_references(submodel_id)
        print(f"✅ Removed Shell references to Submodel '{submodel_id}'.")
