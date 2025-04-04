"""Module for uploading Asset Administration Shell (AAS) files to a server."""

import mimetypes
from pathlib import Path

import requests

from shellsmith.config import DEFAULT_TIMEOUT, config


def upload_aas_folder(path: Path | str) -> None:
    """Uploads all AAS files from a specified folder.

    Accepts `.json`, `.xml`, and `.aasx` files only.

    Args:
        path: The path to the folder containing AAS files.

    Raises:
        ValueError: If the provided path is not a valid directory.
    """
    folder_path = Path(path)

    if not folder_path.is_dir():
        raise ValueError(f"{folder_path} is not a valid directory.")

    for aas_file in folder_path.iterdir():
        if aas_file.is_file() and aas_file.suffix in {".json", ".xml", ".aasx"}:
            print(f"Uploading: '{aas_file.name}'")
            upload_aas(aas_file)


def upload_aas(path: Path | str) -> bool:
    """Uploads a single AAS file to the configured server.

    Acceptable formats: `.json`, `.xml`, `.aasx`.

    Args:
        path: The path to the AAS file. Can be a `Path` or string.

    Returns:
        True if the upload succeeds, otherwise False.
    """
    path = Path(path)
    url = f"{config.host}/upload"

    mime_type, _ = mimetypes.guess_type(path)  # .json, .xml
    if mime_type is None:
        # .aasx
        mime_type = "application/octet-stream"

    with open(path, "rb") as file:
        files = [("file", (path.name, file, mime_type))]
        try:
            response = requests.post(url, files=files, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            success: bool = response.json()
            print(f"✅ Successfully uploaded '{path.name}': {success}")
            return success
        except requests.exceptions.HTTPError as e:
            print(f"❌ Failed to upload '{path.name}': {e}")
            return False
