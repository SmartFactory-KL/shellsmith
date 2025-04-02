"""Handles uploading of AAS files and folders."""

from pathlib import Path

import typer

from shellsmith.cli import args
from shellsmith.upload import upload_aas, upload_aas_folder

app = typer.Typer()


@app.command()
def upload(
    path: Path = args.AAS_PATH,
) -> None:
    """Uploads a single AAS file or all AAS files from a folder.

    Accepts files with `.json`, `.xml`, or `.aasx` extensions.

    Args:
        path: The path to the AAS file or folder to upload.
    """
    if path.is_file():
        print(f"ℹ️ Uploading file: {path}")
        upload_aas(path)
    elif path.is_dir():
        print(f"ℹ️ Uploading all AAS files in folder: {path}")
        upload_aas_folder(path)
    else:
        print(f"❌ Path '{path}' does not exist or is invalid.")
        raise typer.Exit(code=1)
