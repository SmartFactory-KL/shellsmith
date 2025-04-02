"""Deletes all shells and submodels from the AAS environment."""

import typer
from rich.console import Console

from shellsmith import crud
from shellsmith.cli import opts
from shellsmith.cli.commands.info import print_header
from shellsmith.cli.handlers import handle_http_error
from shellsmith.cli.pretty import make_label

app = typer.Typer()


@app.command(name="nuke")
@handle_http_error()
def nuke(host: str = opts.HOST) -> None:
    """Deletes all AAS Shells and Submodels.

    Irreversibly deletes all Shells and Submodels from the AAS environment on the
    specified host. Provides confirmation prompts before performing deletions to
    ensure safety.
    """
    print_header()
    console = Console()

    shells = crud.get_shells(host=host)
    submodels = crud.get_submodels(host=host)

    total_shells = len(shells)
    total_submodels = len(submodels)

    if total_shells == 0 and total_submodels == 0:
        message = "✅ Nothing to delete. The AAS environment is already empty."
        console.print(message, style="green")
        raise typer.Exit()

    console.print("\n☣️  You are about to irreversibly delete:")
    if total_shells:
        console.print(f"  • [cyan]{total_shells} Shell(s)[/cyan]")
    if total_submodels:
        console.print(f"  • [magenta]{total_submodels} Submodel(s)[/magenta]")
    console.print("[bold red]⚠️  This action is IRREVERSIBLE![/bold red]")

    if not typer.confirm("Are you absolutely sure you want to proceed?"):
        console.print("❎ Aborted. No data was deleted.", style="yellow")
        raise typer.Exit()

    # Delete Shells
    if total_shells:
        console.print("\n🔥 Deleting Shells...")
        for shell in shells:
            label = make_label(shell)
            crud.delete_shell(shell["id"], host=host)
            console.print(f"  ✅ Deleted Shell: {label}", style="cyan")

    # Delete Submodels
    if total_submodels:
        console.print("\n🔥 Deleting Submodels...")
        for submodel in submodels:
            label = make_label(submodel)
            crud.delete_submodel(submodel["id"], host=host)
            console.print(f"  ✅ Deleted Submodel: {label}", style="magenta")

    message = "\n🎉 All Shells and Submodels have been deleted."
    console.print(message, style="bold green")
