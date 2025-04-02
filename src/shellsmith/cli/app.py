"""Main CLI entry point for shellsmith with Typer."""

import requests
import typer

from .commands.decode import app as decode_app
from .commands.encode import app as encode_app
from .commands.groups.create import app as create_app
from .commands.groups.delete import app as delete_app
from .commands.groups.get import app as get_app
from .commands.groups.update import app as update_app
from .commands.info import app as info_app
from .commands.nuke import app as nuke_app
from .commands.upload import app as upload_app

app = typer.Typer(
    help="shellsmith - AAS Toolkit command-line interface.",
    no_args_is_help=True,
)

app.add_typer(upload_app)
app.add_typer(info_app)
app.add_typer(nuke_app)
app.add_typer(encode_app)
app.add_typer(decode_app)
app.add_typer(get_app)
app.add_typer(delete_app)
app.add_typer(update_app)
app.add_typer(create_app)


def main() -> None:
    """Main entry point for the CLI."""
    try:
        app()
    except requests.exceptions.ConnectionError as e:
        typer.secho(f"😩 {e}", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"💥 Unexpected error: {e}", fg=typer.colors.RED)
        raise


if __name__ == "__main__":
    main()
