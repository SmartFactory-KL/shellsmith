"""CLI commands for deleting Shells, Submodels, and Submodel Elements."""

import typer

from shellsmith import crud
from shellsmith.cli import args, opts
from shellsmith.cli.handlers import handle_http_error
from shellsmith.cli.pretty import make_label
from shellsmith.extract import collect_submodel_ids

app = typer.Typer(
    name="delete",
    no_args_is_help=True,
    help="Delete Shells, Submodels and Submodel elements.",
)


@app.command("shell")
@handle_http_error()
def delete_shell(
    shell_id: str = args.SHELL_ID,
    cascade: bool = opts.CASCADE,
    host: str = opts.HOST,
) -> None:
    """🔹 Delete a Shell by ID, optionally with its referenced Submodels."""
    if cascade:
        shell = crud.get_shell(shell_id, host=host)
        submodel_ids = collect_submodel_ids(shell)

        for submodel_id in submodel_ids:
            crud.delete_submodel(submodel_id, host=host)
            message = f"✅ Deleted referenced Submodel: {submodel_id}"
            typer.secho(message, fg=typer.colors.YELLOW)

    crud.delete_shell(shell_id, host=host)
    typer.secho(f"✅ Deleted Shell: {shell_id}", fg=typer.colors.GREEN)


@app.command("submodel-ref")
@handle_http_error()
def delete_submodel_ref(
    shell_id: str = args.SHELL_ID,
    submodel_id: str = args.SUBMODEL_ID,
    host: str = opts.HOST,
) -> None:
    """🔹 Delete a Submodel reference from a Shell."""
    crud.delete_submodel_ref(shell_id, submodel_id, host=host)
    message = f"✅ Deleted Submodel reference: {submodel_id} from Shell: {shell_id}"
    typer.secho(message, fg=typer.colors.GREEN)


@app.command("submodel")
@handle_http_error()
def delete_submodel(
    submodel_id: str = args.SUBMODEL_ID,
    remove_refs: bool = opts.REMOVE_REFS,
    host: str = opts.HOST,
) -> None:
    """🔸 Delete a Submodel by ID."""
    if remove_refs:
        shells = crud.get_shells(host=host)
        for shell in shells:
            if submodel_id in collect_submodel_ids(shell):
                label = make_label(shell)
                crud.delete_submodel_ref(shell["id"], submodel_id)
                message = f"🔗 Removed reference from Shell {label}"
                typer.secho(message, fg=typer.colors.YELLOW)

    crud.delete_submodel(submodel_id, host=host)
    message = f"✅ Deleted Submodel: {submodel_id}"
    typer.secho(message, fg=typer.colors.GREEN)


@app.command("element")
def delete_element(
    submodel_id: str = args.SUBMODEL_ID,
    id_short_path: str = args.ID_SHORT_PATH,
    host: str = opts.HOST,
) -> None:
    """🔻 Delete a Submodel Element by idShort path."""
    crud.delete_submodel_element(submodel_id, id_short_path, host=host)
    message = f"✅ Deleted Element {id_short_path} from Submodel {submodel_id}"
    typer.secho(message, fg=typer.colors.GREEN)
