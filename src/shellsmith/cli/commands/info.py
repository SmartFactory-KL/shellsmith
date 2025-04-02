"""Prints structured information about shells and submodels."""

import typer
from rich.align import Align
from rich.console import Console
from rich.panel import Panel

import shellsmith
from shellsmith import services
from shellsmith.cli import opts
from shellsmith.cli.commands.groups import get
from shellsmith.cli.formats import OutputFormat
from shellsmith.cli.handlers import handle_http_error
from shellsmith.cli.pretty import print_data
from shellsmith.config import config

app = typer.Typer()


@app.command(name="info")
@handle_http_error()
def info(host: str = opts.HOST) -> None:
    """Displays the current Shell tree and issues."""
    print_header(host=host)
    get.get_shells(output=OutputFormat.SIMPLE, host=host)
    print_unreferenced_submodels(host=host)
    print_dangling_submodel_refs(host=host)


def print_header(host: str = config.host) -> None:
    """Prints the CLI header with version and host info in a rich box."""
    console = Console()
    version = shellsmith.__version__
    host_status = services.health(host=host)

    body = (
        f"[bold white]shellsmith - AAS Toolkit[/] [dim]v{version}[/]\n"
        f"[cyan]Host:[/] {host} [dim]({host_status})[/]"
    )
    panel = Panel(
        body,
        title=":information: Info",
        expand=False,
        border_style="bold blue",
    )
    panel = Align.center(panel, vertical="middle")
    console.print(panel)


def print_unreferenced_submodels(host: str = config.host) -> None:
    """Displays Submodels that are not referenced by any Shell."""
    submodel_ids = services.find_unreferenced_submodels(host)

    if submodel_ids:
        submodels = []
        for submodel_id in submodel_ids:
            submodel = shellsmith.get_submodel(submodel_id)
            id_short = submodel.get("idShort", "<no idShort>")
            submodels.append({id_short: submodel_id})
        typer.echo()
        data = [{"": "", "submodels": submodels}]
        print_data(data, OutputFormat.SIMPLE, title="⚠️ Unreferenced Submodels")


def print_dangling_submodel_refs(host: str = config.host) -> None:
    """Displays Shell-to-Submodel references that point to missing Submodels."""
    dangling = services.find_dangling_submodel_refs(host)

    if dangling:
        typer.echo()
        print_data(dangling, OutputFormat.SIMPLE, "⚠️ Dangling Submodel References")
