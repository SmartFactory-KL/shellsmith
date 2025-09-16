"""MCP server for shellsmith BaSyx integration."""

import logging

from fastmcp import FastMCP

from shellsmith.clients import AsyncClient
from shellsmith.config import config

logger = logging.getLogger(__name__)

app = FastMCP(name="shellsmith")


@app.tool()
async def get_shells(host: str = config.host) -> dict:
    """Retrieves all Shells from the AAS server.

    Corresponds to:
    GET /shells

    Args:
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A list of dictionaries representing the Shells.

    Raises:
        HTTPError: If the GET request fails.
    """
    async with AsyncClient(host=host) as client:
        return await client.get_shells()


@app.tool()
async def get_shell(
    shell_id: str, encode: bool = True, host: str = config.host
) -> dict:
    """Retrieves a specific Shell by its ID.

    Corresponds to:
    GET /shells/{shell_id}

    Args:
        shell_id: The unique identifier of the Shell.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the Shell.

    Raises:
        HTTPError: If the GET request fails.
    """
    async with AsyncClient(host=host) as client:
        return await client.get_shell(shell_id, encode=encode)


@app.tool()
async def create_shell(shell: dict, host: str = config.host) -> dict:
    """Creates a new Shell on the AAS server.

    Corresponds to:
    POST /shells

    Args:
        shell: A dictionary representing the Shell to be created.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the created Shell.

    Raises:
        HTTPError: If the POST request fails.
    """
    async with AsyncClient(host=host) as client:
        return await client.create_shell(shell)


@app.tool()
async def update_shell(
    shell_id: str, shell: dict, encode: bool = True, host: str = config.host
) -> None:
    """Updates an existing Shell on the AAS server by its ID.

    Corresponds to:
    PUT /shells/{shell_id}

    Args:
        shell_id: The unique identifier of the Shell.
        shell: A dictionary representing the updated Shell content.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the PUT request fails.
    """
    async with AsyncClient(host=host) as client:
        await client.update_shell(shell_id, shell, encode=encode)


@app.tool()
async def delete_shell(
    shell_id: str, encode: bool = True, host: str = config.host
) -> None:
    """Deletes a specific Shell by its ID.

    Corresponds to:
    DELETE /shells/{shell_id}

    Args:
        shell_id: The unique identifier of the Shell.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the DELETE request fails.
    """
    async with AsyncClient(host=host) as client:
        await client.delete_shell(shell_id, encode=encode)


@app.tool()
async def get_submodel_refs(
    shell_id: str, encode: bool = True, host: str = config.host
) -> dict:
    """Retrieves all submodel references from a specific Shell.

    Corresponds to:
    GET /shells/{shell_id}/submodel-refs

    Args:
        shell_id: The unique identifier of the Shell.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A list of dictionaries representing the submodel references.

    Raises:
        HTTPError: If the GET request fails.
    """
    async with AsyncClient(host=host) as client:
        return await client.get_submodel_refs(shell_id, encode=encode)


@app.tool()
async def create_submodel_ref(
    shell_id: str, submodel_ref: dict, encode: bool = True, host: str = config.host
) -> None:
    """Creates a submodel reference for a specific Shell.

    Corresponds to:
    POST /shells/{shell_id}/submodel-refs

    Args:
        shell_id: The unique identifier of the Shell.
        submodel_ref: A dictionary representing the submodel reference to be added.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the POST request fails.
    """
    async with AsyncClient(host=host) as client:
        await client.create_submodel_ref(shell_id, submodel_ref, encode=encode)


@app.tool()
async def delete_submodel_ref(
    shell_id: str, submodel_id: str, encode: bool = True, host: str = config.host
) -> None:
    """Deletes a specific submodel reference from a Shell.

    Corresponds to:
    DELETE /shells/{shell_id}/submodel-refs/{submodel_id}

    Args:
        shell_id: The unique identifier of the Shell.
        submodel_id: The unique identifier of the submodel.
        encode: Whether to Base64-encode both identifiers. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the DELETE request fails.
    """
    async with AsyncClient(host=host) as client:
        await client.delete_submodel_ref(shell_id, submodel_id, encode=encode)


@app.tool()
async def get_submodels(host: str = config.host) -> dict:
    """Retrieves all Submodels from the AAS server.

    Corresponds to:
    GET /submodels

    Args:
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A list of dictionaries representing the Submodels.

    Raises:
        HTTPError: If the GET request fails.
    """
    async with AsyncClient(host=host) as client:
        return await client.get_submodels()


@app.tool()
async def get_submodel(
    submodel_id: str, encode: bool = True, host: str = config.host
) -> dict:
    """Retrieves a specific Submodel by its ID.

    Corresponds to:
    GET /submodels/{submodel_id}

    Args:
        submodel_id: The unique identifier of the submodel.
        encode: Whether to Base64-encode the submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the submodel.

    Raises:
        HTTPError: If the GET request fails.
    """
    async with AsyncClient(host=host) as client:
        return await client.get_submodel(submodel_id, encode=encode)


@app.tool()
async def create_submodel(submodel: dict, host: str = config.host) -> dict:
    """Creates a new Submodel on the AAS server.

    Corresponds to:
    POST /submodels

    Args:
        submodel: A dictionary representing the Submodel to be created.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the created Submodel.

    Raises:
        HTTPError: If the POST request fails.
    """
    async with AsyncClient(host=host) as client:
        return await client.create_submodel(submodel)


@app.tool()
async def update_submodel(
    submodel_id: str, submodel: dict, encode: bool = True, host: str = config.host
) -> None:
    """Updates an existing Submodel by its ID.

    Corresponds to:
    PUT /submodels/{submodel_id}

    Args:
        submodel_id: The unique identifier of the Submodel.
        submodel: A dictionary representing the updated Submodel content.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the PUT request fails.
    """
    async with AsyncClient(host=host) as client:
        await client.update_submodel(submodel_id, submodel, encode=encode)


@app.tool()
async def delete_submodel(
    submodel_id: str, encode: bool = True, host: str = config.host
) -> None:
    """Deletes a specific Submodel by its ID.

    Corresponds to:
    DELETE /submodels/{submodel_id}

    Args:
        submodel_id: The unique identifier of the Submodel.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the DELETE request fails.
    """
    async with AsyncClient(host=host) as client:
        await client.delete_submodel(submodel_id, encode=encode)


@app.tool()
async def get_submodel_value(
    submodel_id: str, encode: bool = True, host: str = config.host
) -> dict:
    """Retrieves the raw value of a specific Submodel.

    Corresponds to:
    GET /submodels/{submodel_id}/$value

    Args:
        submodel_id: The unique identifier of the Submodel.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the Submodel value.

    Raises:
        HTTPError: If the GET request fails.
    """
    async with AsyncClient(host=host) as client:
        return await client.get_submodel_value(submodel_id, encode=encode)


@app.tool()
async def update_submodel_value(
    submodel_id: str,
    value: list[dict],
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Updates the value of a specific Submodel.

    Corresponds to:
    PATCH /submodels/{submodel_id}/$value

    Args:
        submodel_id: The unique identifier of the Submodel.
        value: A list[dict] representing the updated Submodel value.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the updated Submodel value.

    Raises:
        HTTPError: If the PATCH request fails.
    """
    async with AsyncClient(host=host) as client:
        await client.update_submodel_value(submodel_id, value, encode=encode)


@app.tool()
async def get_submodel_metadata(
    submodel_id: str, encode: bool = True, host: str = config.host
) -> dict:
    """Retrieves the metadata of a specific Submodel.

    Corresponds to:
    GET /submodels/{submodel_id}/$metadata

    Args:
        submodel_id: The unique identifier of the Submodel.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the Submodel metadata.

    Raises:
        HTTPError: If the GET request fails.
    """
    async with AsyncClient(host=host) as client:
        return await client.get_submodel_metadata(submodel_id, encode=encode)


@app.tool()
async def get_submodel_elements(
    submodel_id: str, encode: bool = True, host: str = config.host
) -> dict:
    """Retrieves all Submodel elements from a specific Submodel.

    Corresponds to:
    GET /submodels/{submodel_id}/submodel-elements

    Args:
        submodel_id: The unique identifier of the Submodel.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A list of dictionaries representing the Submodel elements.

    Raises:
        HTTPError: If the GET request fails.
    """
    async with AsyncClient(host=host) as client:
        return await client.get_submodel_elements(submodel_id, encode=encode)


@app.tool()
async def create_submodel_element(
    submodel_id: str,
    element: dict,
    id_short_path: str | None = None,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Creates a Submodel element.

    If `id_short_path` is given, creates the element at that nested path.
    Otherwise, creates the element at the root level.

    Corresponds to:
    POST /submodels/{submodel_id}/submodel-elements
    POST /submodels/{submodel_id}/submodel-elements/{idShortPath}

    Args:
        submodel_id: The unique identifier of the Submodel.
        element: A dictionary representing the Submodel element to create.
        id_short_path: The idShort path for the new Submodel element.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the POST request fails.
    """
    async with AsyncClient(host=host) as client:
        await client.create_submodel_element(
            submodel_id, element, id_short_path, encode=encode
        )


@app.tool()
async def get_submodel_element(
    submodel_id: str, id_short_path: str, encode: bool = True, host: str = config.host
) -> dict:
    """Retrieves a specific Submodel element by its idShort path.

    Corresponds to:
    GET /submodels/{submodel_id}/submodel-elements/{id_short_path}

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the submodel element.

    Raises:
        HTTPError: If the GET request fails.
    """
    async with AsyncClient(host=host) as client:
        return await client.get_submodel_element(
            submodel_id, id_short_path, encode=encode
        )


@app.tool()
async def update_submodel_element(
    submodel_id: str,
    id_short_path: str,
    element: dict,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Updates or creates a Submodel element by full replacement.

    Corresponds to:
    PUT /submodels/{submodel_id}/submodel-elements/{idShortPath}

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
        element: A dictionary representing the new element content.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the PUT request fails.
    """
    async with AsyncClient(host=host) as client:
        await client.update_submodel_element(
            submodel_id, id_short_path, element, encode=encode
        )


@app.tool()
async def delete_submodel_element(
    submodel_id: str, id_short_path: str, encode: bool = True, host: str = config.host
) -> None:
    """Deletes a specific Submodel element by its idShort path.

    Corresponds to:
    DELETE /submodels/{submodel_id}/submodel-elements/{idShortPath}

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the DELETE request fails.
    """
    async with AsyncClient(host=host) as client:
        await client.delete_submodel_element(submodel_id, id_short_path, encode=encode)


@app.tool()
async def get_submodel_element_value(
    submodel_id: str, id_short_path: str, encode: bool = True, host: str = config.host
) -> dict | list | str | int | float | bool | None:
    """Retrieves the raw value of a specific Submodel element.

    Corresponds to:
    GET /submodels/{submodel_id}/submodel-elements/{idShortPath}/$value

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the raw value.

    Raises:
        HTTPError: If the GET request fails.
    """
    async with AsyncClient(host=host) as client:
        return await client.get_submodel_element_value(
            submodel_id, id_short_path, encode=encode
        )


@app.tool()
async def update_submodel_element_value(
    submodel_id: str,
    id_short_path: str,
    value: str,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Updates the value of a specific Submodel element.

    Corresponds to:
    PATCH /submodels/{submodel_id}/submodel-elements/{id_short_path}/$value

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
        value: The new value to assign to the Submodel element.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the PATCH request fails.
    """
    async with AsyncClient(host=host) as client:
        await client.update_submodel_element_value(
            submodel_id, id_short_path, value, encode=encode
        )


@app.tool()
async def get_health_status(
    host: str = config.host, timeout: float = config.timeout
) -> str:
    """Check health status of the AAS environment.

    Args:
        host: Base URL of the AAS server. Defaults to configured host.
        timeout: Request timeout in seconds. Defaults to configured timeout.

    Returns:
        Health status string.
    """
    async with AsyncClient(host=host, timeout=timeout) as client:
        return await client.get_health_status()


@app.tool()
async def is_healthy(host: str = config.host, timeout: float = config.timeout) -> bool:
    """Check if the AAS environment is ready for requests.

    Args:
        host: Base URL of the AAS server. Defaults to configured host.
        timeout: Request timeout in seconds. Defaults to configured timeout.

    Returns:
        True if healthy, False otherwise.
    """
    async with AsyncClient(host=host, timeout=timeout) as client:
        return await client.is_healthy()


async def main() -> None:
    """Run the MCP server."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting shellsmith MCP server")
    await app.run()


def cli_main() -> None:
    """CLI entry point for the MCP server."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting shellsmith MCP server")
    app.run()


if __name__ == "__main__":
    cli_main()
