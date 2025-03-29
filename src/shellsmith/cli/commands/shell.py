"""Handles deletion of Asset Administration Shells."""

import requests.exceptions

import shellsmith
from shellsmith import services


def shell_delete(shell_id: str, cascade: bool = False) -> None:
    """Deletes a Shell by ID, optionally cascading to its Submodels.

    Args:
        shell_id: The unique identifier of the Shell to delete.
        cascade: If True, also deletes all referenced submodels.
    """
    print(f"🗑️ Deleting Shell: {shell_id}")
    try:
        if cascade:
            services.delete_shell_cascading(shell_id)
            print(f"✅ Shell '{shell_id}' and its submodels deleted.")
        else:
            shellsmith.delete_shell(shell_id)
            print(f"✅ Shell '{shell_id}' deleted.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Failed to delete Shell '{shell_id}': {e}")
