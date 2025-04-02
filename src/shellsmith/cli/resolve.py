"""Utility functions for resolving CLI input sources."""

import json
from pathlib import Path

import typer
import yaml

from shellsmith.utils import load_data


def resolve_input(
    data: str | None, file: Path | None
) -> dict | list | str | int | float | bool | None:
    """Resolves input from --data (expects JSON) or --file (supports JSON/YAML)."""
    if data and file:
        typer.secho("❌ Use either --data or --file, not both.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if not data and not file:
        typer.secho("❌ Provide either --data or --file.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    try:
        if data:
            return json.loads(data)  # Strictly JSON for inline input
        return load_data(file)  # Flexible for files (JSON or YAML)
    except (json.JSONDecodeError, yaml.YAMLError, OSError, ValueError) as e:
        typer.secho(f"❌ Failed to parse input: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1) from e
