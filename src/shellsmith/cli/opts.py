"""Reusable CLI options in commands."""

import typer

from shellsmith.config import config

from .formats import OutputFormat

OUTPUT: typer.Option = typer.Option(
    OutputFormat.SIMPLE,
    help="The output format.",
)

HOST: typer.Option = typer.Option(
    config.host,
    help="The AAS Environment host for the command.",
)

CASCADE = typer.Option(
    False,
    "--cascade",
    help="Also delete all submodels referenced by this Shell.",
)

REMOVE_REFS = typer.Option(
    False,
    "--remove-refs",
    help="Also remove all references to the Submodel.",
)

DATA: typer.Option = typer.Option(
    None,
    "--data",
    help="Inline JSON data string.",
)

FILE: typer.Option = typer.Option(
    None,
    "--file",
    help="Path to JSON or YAML file containing the data.",
)
