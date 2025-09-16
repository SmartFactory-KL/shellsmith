"""Module for uploading Asset Administration Shell (AAS) files to a server.

Deprecated: These functions are now methods on Client and AsyncClient classes.
Use Client().upload_aas() or AsyncClient.upload_aas() instead.
These functions are kept for backwards compatibility.
"""

from pathlib import Path

from shellsmith.clients import Client


def upload_aas_folder(path: Path | str) -> None:
    """Uploads all AAS files from a specified folder.

    Deprecated: Use Client().upload_aas_folder() instead.

    Accepts `.json`, `.xml`, and `.aasx` files only.

    Args:
        path: The path to the folder containing AAS files.

    Raises:
        ValueError: If the provided path is not a valid directory.
    """
    with Client() as client:
        client.upload_aas_folder(path)


def upload_aas(path: Path | str) -> bool:
    """Uploads a single AAS file to the configured server.

    Deprecated: Use Client().upload_aas() instead.

    Acceptable formats: `.json`, `.xml`, `.aasx`.

    Args:
        path: The path to the AAS file. Can be a `Path` or string.

    Returns:
        True if the upload succeeds, otherwise False.
    """
    with Client() as client:
        return client.upload_aas(path)
