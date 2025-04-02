"""Reusable CLI arguments in commands."""

import typer

SHELL_ID: typer.Argument = typer.Argument(
    ...,
    help="The unique identifier of the Shell.",
)

SUBMODEL_ID: typer.Argument = typer.Argument(
    ...,
    help="The unique identifier of the Submodel.",
)

ID_SHORT_PATH: typer.Argument = typer.Argument(
    ...,
    help="The idShort path for the Submodel Element.",
)

OPTIONAL_ID_SHORT_PATH: typer.Argument = typer.Argument(
    None,
    help="Optional idShort path for a nested Submodel Element.",
)

AAS_PATH: typer.Argument = typer.Argument(
    ...,
    help="The path to the AAS file or folder to upload. Accepts: .json, .xml, .aasx",
)

VALUE: typer.Argument = typer.Argument(..., help="The new value as string.")
