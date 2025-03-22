from pathlib import Path

from shellsmith.upload import upload_aas, upload_aas_folder


def upload(path: Path):
    if path.is_file():
        print(f"ℹ️ Uploading file: {path}")
        upload_aas(path)
    elif path.is_dir():
        print(f"ℹ️ Uploading all AAS files in folder: {path}")
        upload_aas_folder(path)
    else:
        print(f"❌ Path '{path}' does not exist or is invalid.")
