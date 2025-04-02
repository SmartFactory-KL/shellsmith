"""CLI decorators for consistent error handling."""

from collections.abc import Callable
from functools import wraps

import typer
from requests import HTTPError


def handle_http_error() -> Callable:
    """Wraps a CLI command to catch HTTPError and exit cleanly.

    This decorator intercepts requests.exceptions.HTTPError raised in CLI command
    functions, logs the error with the provided kwargs as context,
    and exits with code 1.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: object, **kwargs: object) -> None:
            try:
                return func(*args, **kwargs)
            except HTTPError as error:
                params = " ".join(f"{k}={v}" for k, v in kwargs.items())
                message = f"⚠️ {error}: {params}"
                typer.secho(message, fg=typer.colors.YELLOW)
                raise typer.Exit(code=1) from error

        return wrapper

    return decorator
