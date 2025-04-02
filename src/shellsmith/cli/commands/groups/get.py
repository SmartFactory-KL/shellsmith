"""CLI commands for retrieving AAS Shells, Submodels, and Submodel Elements."""

import typer

from shellsmith import crud
from shellsmith.cli import args, opts
from shellsmith.cli.formats import OutputFormat
from shellsmith.cli.handlers import handle_http_error
from shellsmith.cli.pretty import print_data
from shellsmith.cli.simplify import enrich, simplify, simplify_element

app = typer.Typer(
    name="get",
    no_args_is_help=True,
    help="Get Shells, Submodels and Submodel Elements.",
)


# ───────────────────────────────────── Shells ─────────────────────────────────────────


@app.command(name="shells")
@handle_http_error()
def get_shells(output: OutputFormat = opts.OUTPUT, host: str = opts.HOST) -> None:
    """🔹 Get all available Shells."""
    shells = crud.get_shells(host)

    if output == OutputFormat.SIMPLE:
        shells = [enrich(simplify(shell), host) for shell in shells]

    print_data(shells, output_format=output, title="🐌 Shells")


@app.command(name="shell")
@handle_http_error()
def get_shell(
    shell_id: str = args.SHELL_ID,
    output: OutputFormat = opts.OUTPUT,
    host: str = opts.HOST,
) -> None:
    """🔹 Get a specific Shell."""
    shell = crud.get_shell(shell_id, host=host)

    if output == OutputFormat.SIMPLE:
        shell = [enrich(simplify(shell), host)]

    print_data(shell, output_format=output, title="🐌 Shell")


@app.command(name="submodel-refs")
@handle_http_error()
def get_submodel_refs(
    shell_id: str = args.SHELL_ID,
    host: str = opts.HOST,
) -> None:
    """🔹 Get all Submodel References of a specific Shell."""
    submodel_refs = crud.get_submodel_refs(shell_id, host=host)
    print_data(submodel_refs, output_format=OutputFormat.JSON)


# ─────────────────────────────────── Submodels ────────────────────────────────────────


@app.command(name="submodels")
@handle_http_error()
def get_submodels(output: OutputFormat = opts.OUTPUT, host: str = opts.HOST) -> None:
    """🔸 Get all available Submodels."""
    submodels = crud.get_submodels(host)

    if output == OutputFormat.SIMPLE:
        submodels = [simplify(submodel) for submodel in submodels]

    print_data(submodels, output_format=output, title="📦 Submodels")


@app.command(name="submodel")
@handle_http_error()
def get_submodel(
    submodel_id: str = args.SUBMODEL_ID,
    output: OutputFormat = opts.OUTPUT,
    host: str = opts.HOST,
) -> None:
    """🔸 Get a specific Submodel."""
    submodel = crud.get_submodel(submodel_id, host=host)

    if output == OutputFormat.SIMPLE:
        submodel = [enrich(simplify(submodel), host)]

    print_data(submodel, output_format=output, title="📦 Submodel")


@app.command(name="submodel-value")
@handle_http_error()
def get_submodel_value(
    submodel_id: str = args.SUBMODEL_ID,
    host: str = opts.HOST,
) -> None:
    """🔸 Get the $value of a specific Submodel."""
    value = crud.get_submodel_value(submodel_id, host=host)
    print_data(value, output_format=OutputFormat.PLAIN)


@app.command(name="submodel-meta")
@handle_http_error()
def get_submodel_meta(
    submodel_id: str = args.SUBMODEL_ID,
    host: str = opts.HOST,
) -> None:
    """🔸 Get the $metadata of a specific Submodel."""
    metadata = crud.get_submodel_metadata(submodel_id, host=host)
    print_data(metadata, output_format=OutputFormat.PLAIN)


# ─────────────────────────────── Submodel Elements ────────────────────────────────────


@app.command(name="elements")
@handle_http_error()
def get_submodel_elements(
    submodel_id: str = args.SUBMODEL_ID,
    output: OutputFormat = opts.OUTPUT,
    host: str = opts.HOST,
) -> None:
    """🔻 Get all Submodel Elements of a specific Submodel."""
    submodel_elements = crud.get_submodel_elements(submodel_id, host=host)
    if output == OutputFormat.SIMPLE:
        submodel_elements = [simplify_element(element) for element in submodel_elements]
        output = OutputFormat.TREE
    print_data(
        submodel_elements,
        output_format=output,
        title="🧩 Submodel Elements",
    )


@app.command(name="element")
@handle_http_error()
def get_submodel_element(
    submodel_id: str = args.SUBMODEL_ID,
    id_short_path: str = args.ID_SHORT_PATH,
    output: OutputFormat = opts.OUTPUT,
    host: str = opts.HOST,
) -> None:
    """🔻 Get a specific Submodel Element."""
    submodel_element = crud.get_submodel_element(submodel_id, id_short_path, host=host)
    if output == OutputFormat.SIMPLE:
        submodel_element = [simplify_element(submodel_element)]
        output = OutputFormat.TREE
    print_data(
        submodel_element,
        output_format=output,
        title="🧩 Submodel Element",
    )


@app.command(name="element-value")
@handle_http_error()
def get_submodel_element_value(
    submodel_id: str = args.SUBMODEL_ID,
    id_short_path: str = args.ID_SHORT_PATH,
    host: str = opts.HOST,
) -> None:
    """🔻 Get the $value of a specific Submodel Element."""
    value = crud.get_submodel_element_value(submodel_id, id_short_path, host=host)
    print_data(value, output_format=OutputFormat.PLAIN)
