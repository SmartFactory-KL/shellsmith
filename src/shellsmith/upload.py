import mimetypes
from pathlib import Path

import requests

from shellsmith.config import config


def upload_aas_folder(path: Path | str):
    folder_path = Path(path)

    if not folder_path.is_dir():
        raise ValueError(f"{folder_path} is not a valid directory.")

    for aas_file in folder_path.iterdir():
        if aas_file.is_file() and aas_file.suffix in {".json", ".xml", ".aasx"}:
            print(f"Uploading: '{aas_file.name}'")
            upload_aas(aas_file)


def upload_aas(path: Path | str):
    path = Path(path)
    url = f"{config.host}/upload"

    mime_type, _ = mimetypes.guess_type(path)
    if mime_type is None:
        # .aasx
        mime_type = "application/octet-stream"

    with open(path, "rb") as file:
        files = [("file", (path.name, file, mime_type))]
        try:
            response = requests.post(url, files=files)
            response.raise_for_status()
            success = response.json()
            print(f"✅ Successfully uploaded '{path.name}': {success}")
            return success
        except requests.exceptions.HTTPError as e:
            print(f"❌ Failed to upload '{path.name}': {e}")
            return False
