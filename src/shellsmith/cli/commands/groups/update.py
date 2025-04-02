"""CLI commands for updating Shells, Submodels, and Submodel Elements."""

from pathlib import Path

import typer

from shellsmith import crud
from shellsmith.cli import args, opts
from shellsmith.cli.handlers import handle_http_error
from shellsmith.cli.resolve import resolve_input

app = typer.Typer(
    name="update",
    no_args_is_help=True,
    help="Update Shells, Submodels and Submodel elements.",
)


@app.command("shell")
@handle_http_error()
def update_shell(
    shell_id: str = args.SHELL_ID,
    data: str | None = opts.DATA,
    file: Path | None = opts.FILE,
    host: str = opts.HOST,
) -> None:
    """🔹 Update a Shell by ID (full replacement).

    This operation performs a full replacement (PUT) of the Shell.
    The provided payload must include the entire Shell object.
    """
    payload = resolve_input(data, file)
    crud.put_shell(shell_id, payload, host=host)
    typer.secho(f"✅ Updated Shell: {shell_id}", fg=typer.colors.GREEN)


@app.command("submodel")
@handle_http_error()
def update_submodel(
    submodel_id: str = args.SUBMODEL_ID,
    data: str | None = opts.DATA,
    file: Path | None = opts.FILE,
    host: str = opts.HOST,
) -> None:
    """🔸 Update a Submodel by ID (full replacement).

    This operation performs a full replacement (PUT) of the Submodel.
    The entire Submodel structure must be provided in the payload.
    """
    payload = resolve_input(data, file)
    crud.put_submodel(submodel_id, payload, host=host)
    typer.secho(f"✅ Updated Submodel: {submodel_id}", fg=typer.colors.GREEN)


@app.command("submodel-value")
@handle_http_error()
def update_submodel_value(
    submodel_id: str = args.SUBMODEL_ID,
    data: str | None = opts.DATA,
    file: Path | None = opts.FILE,
    host: str = opts.HOST,
) -> None:
    """🔸 Update the $value of a Submodel (partial update).

    This operation performs a partial update (PATCH) and updates only existing fields.
    New fields will not be added.
    ⚠️ Currently not supported by BaSyx — will result in a 400 error.
    """
    payload = resolve_input(data, file)
    crud.patch_submodel_value(submodel_id, payload, host=host)
    typer.secho(f"✅ Updated Submodel value: {submodel_id}", fg=typer.colors.GREEN)


@app.command("element")
@handle_http_error()
def update_element(
    submodel_id: str = args.SUBMODEL_ID,
    id_short_path: str = args.ID_SHORT_PATH,
    data: str | None = opts.DATA,
    file: Path | None = opts.FILE,
    host: str = opts.HOST,
) -> None:
    """🔻 Update a Submodel Element by idShort path (full replacement).

    This operation replaces the full Submodel Element using PUT.
    """
    payload = resolve_input(data, file)
    crud.put_submodel_element(submodel_id, id_short_path, payload, host=host)
    typer.secho(
        f"✅ Updated Submodel Element: {id_short_path} in Submodel {submodel_id}",
        fg=typer.colors.GREEN,
    )


@app.command("element-value")
@handle_http_error()
def update_element_value(
    submodel_id: str = args.SUBMODEL_ID,
    id_short_path: str = args.ID_SHORT_PATH,
    value: str = args.VALUE,
    host: str = opts.HOST,
) -> None:
    """🔻 Update the $value of a Submodel Element (partial update).

    This uses PATCH to modify only the value field.
    """
    crud.patch_submodel_element_value(submodel_id, id_short_path, value, host=host)
    typer.secho(
        f"✅ Updated value of Element {id_short_path} in Submodel {submodel_id}",
        fg=typer.colors.GREEN,
    )
