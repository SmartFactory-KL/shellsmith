"""CLI command for base64-encoding unique identifiers."""

import typer

from shellsmith.utils import base64_encode

app = typer.Typer()


@app.command("encode")
def encode(value: str) -> None:
    """Encodes a value to Base64."""
    print(base64_encode(value))
