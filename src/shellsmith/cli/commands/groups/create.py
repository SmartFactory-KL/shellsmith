"""CLI commands for creating Shells, Submodels, and Submodel Elements."""

from pathlib import Path

import typer

from shellsmith import crud
from shellsmith.cli import args, opts
from shellsmith.cli.handlers import handle_http_error
from shellsmith.cli.pretty import make_label
from shellsmith.cli.resolve import resolve_input

app = typer.Typer(
    name="create",
    no_args_is_help=True,
    help="Create Shells, Submodels and Submodel elements.",
)


@app.command("shell")
@handle_http_error()
def create_shell(
    data: str | None = opts.DATA,
    file: Path | None = opts.FILE,
    host: str = opts.HOST,
) -> None:
    """🔹 Create a Shell from a data payload."""
    payload = resolve_input(data, file)
    created = crud.post_shell(payload, host=host)
    label = make_label(created)
    typer.secho(f"✅ Created Shell: {label}", fg=typer.colors.GREEN)


@app.command("submodel-ref")
@handle_http_error()
def create_submodel_ref(
    shell_id: str = args.SHELL_ID,
    data: str | None = opts.DATA,
    file: Path | None = opts.FILE,
    host: str = opts.HOST,
) -> None:
    """🔹 Create a Submodel reference for a Shell."""
    payload = resolve_input(data, file)
    crud.post_submodel_ref(shell_id, payload, host=host)
    message = f"✅ Created Submodel reference in Shell: {shell_id}"
    typer.secho(message, fg=typer.colors.GREEN)


@app.command("submodel")
@handle_http_error()
def create_submodel(
    data: str | None = opts.DATA,
    file: Path | None = opts.FILE,
    host: str = opts.HOST,
) -> None:
    """🔸 Create a Submodel from a data payload."""
    payload = resolve_input(data, file)
    created = crud.post_submodel(payload, host=host)
    label = make_label(created)
    typer.secho(f"✅ Created Submodel: {label}", fg=typer.colors.GREEN)


@app.command("element")
@handle_http_error()
def create_element(
    submodel_id: str = args.SUBMODEL_ID,
    id_short_path: str | None = args.OPTIONAL_ID_SHORT_PATH,
    data: str | None = opts.DATA,
    file: Path | None = opts.FILE,
    host: str = opts.HOST,
) -> None:
    """🔻 Create a Submodel Element (root or nested)."""
    payload = resolve_input(data, file)
    crud.post_submodel_element(submodel_id, payload, id_short_path, host=host)
    label = (
        f"nested Element: {id_short_path}" if id_short_path else "root-level Element"
    )
    message = f"✅ Created {label} in Submodel: {submodel_id}"
    typer.secho(message, fg=typer.colors.GREEN)
