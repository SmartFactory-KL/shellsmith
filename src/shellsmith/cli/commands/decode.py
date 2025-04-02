"""CLI command for base64-decoding unique identifiers."""

import typer

from shellsmith.utils import base64_decode

app = typer.Typer()


@app.command()
def decode(value: str) -> None:
    """Decodes a Base64 value."""
    print(base64_decode(value))
