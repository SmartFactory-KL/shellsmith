"""Convenience functions for AAS operations using temporary clients.

This module provides httpx-style convenience functions that create temporary
clients internally, similar to httpx.get(), httpx.post(), etc.
"""

from typing import Any

from shellsmith.clients import Client
from shellsmith.config import config
from shellsmith.types import JSON

# ───────────────────────────────────── Shells ─────────────────────────────────────────


def get_shells(host: str = config.host) -> dict:
    """Retrieve all shells.

    Args:
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A list of dictionaries representing the Shells.

    Raises:
        HTTPError: If the GET request fails.
    """
    with Client(host=host) as client:
        return client.get_shells()


def get_shell(shell_id: str, encode: bool = True, host: str = config.host) -> dict:
    """Retrieve a specific shell by ID.

    Args:
        shell_id: The unique identifier of the Shell.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the Shell.

    Raises:
        HTTPError: If the GET request fails.
    """
    with Client(host=host) as client:
        return client.get_shell(shell_id, encode)


def create_shell(shell: dict, host: str = config.host) -> dict:
    """Create a new shell.

    Args:
        shell: A dictionary representing the Shell to be created.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the created Shell.

    Raises:
        HTTPError: If the POST request fails.
    """
    with Client(host=host) as client:
        return client.create_shell(shell)


def update_shell(
    shell_id: str,
    shell: dict,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Update an existing shell.

    Args:
        shell_id: The unique identifier of the Shell.
        shell: A dictionary representing the updated Shell content.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the PUT request fails.
    """
    with Client(host=host) as client:
        client.update_shell(shell_id, shell, encode)


def delete_shell(shell_id: str, encode: bool = True, host: str = config.host) -> None:
    """Delete a shell by ID.

    Args:
        shell_id: The unique identifier of the Shell.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the DELETE request fails.
    """
    with Client(host=host) as client:
        client.delete_shell(shell_id, encode)


def get_submodel_refs(
    shell_id: str,
    encode: bool = True,
    host: str = config.host,
    **kwargs: Any,
) -> dict:
    """Retrieve all submodel references from a specific Shell.

    Args:
        shell_id: The unique identifier of the Shell.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.Args:
        **kwargs: Additional keyword arguments to pass to the request.

    Returns:
        A list of dictionaries representing the submodel references.

    Raises:
        HTTPError: If the GET request fails.
    """
    with Client(host=host) as client:
        return client.get_submodel_refs(shell_id, encode, **kwargs)


def create_submodel_ref(
    shell_id: str,
    submodel_ref: dict,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Create a submodel reference for a specific Shell.

    Args:
        shell_id: The unique identifier of the Shell.
        submodel_ref: A dictionary representing the submodel reference to be added.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the POST request fails.
    """
    with Client(host=host) as client:
        client.create_submodel_ref(shell_id, submodel_ref, encode)


def delete_submodel_ref(
    shell_id: str,
    submodel_id: str,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Delete a specific submodel reference from a Shell.

    Args:
        shell_id: The unique identifier of the Shell.
        submodel_id: The unique identifier of the submodel.
        encode: Whether to Base64-encode both identifiers. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the DELETE request fails.
    """
    with Client(host=host) as client:
        client.delete_submodel_ref(shell_id, submodel_id, encode)


# ─────────────────────────────────── Sync Submodels ───────────────────────────────────


def get_submodels(host: str = config.host) -> dict:
    """Retrieve all submodels.

    Args:
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A list of dictionaries representing the Submodels.

    Raises:
        HTTPError: If the GET request fails.
    """
    with Client(host=host) as client:
        return client.get_submodels()


def get_submodel(
    submodel_id: str,
    encode: bool = True,
    host: str = config.host,
) -> dict:
    """Retrieve a specific submodel by ID.

    Args:
        submodel_id: The unique identifier of the submodel.
        encode: Whether to Base64-encode the submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the submodel.

    Raises:
        HTTPError: If the GET request fails.
    """
    with Client(host=host) as client:
        return client.get_submodel(submodel_id, encode)


def create_submodel(submodel: dict, host: str = config.host) -> dict:
    """Create a new submodel.

    Args:
        submodel: A dictionary representing the Submodel to be created.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the created Submodel.

    Raises:
        HTTPError: If the POST request fails.
    """
    with Client(host=host) as client:
        return client.create_submodel(submodel)


def update_submodel(
    submodel_id: str,
    submodel: dict,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Update an existing submodel.

    Args:
        submodel_id: The unique identifier of the Submodel.
        submodel: A dictionary representing the updated Submodel content.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the PUT request fails.
    """
    with Client(host=host) as client:
        client.update_submodel(submodel_id, submodel, encode)


def delete_submodel(
    submodel_id: str,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Delete a submodel by ID.

    Args:
        submodel_id: The unique identifier of the Submodel.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the DELETE request fails.
    """
    with Client(host=host) as client:
        client.delete_submodel(submodel_id, encode)


def get_submodel_value(
    submodel_id: str,
    encode: bool = True,
    host: str = config.host,
) -> dict:
    """Retrieve the raw value of a specific Submodel.

    Args:
        submodel_id: The unique identifier of the Submodel.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the Submodel value.

    Raises:
        HTTPError: If the GET request fails.
    """
    with Client(host=host) as client:
        return client.get_submodel_value(submodel_id, encode)


def update_submodel_value(
    submodel_id: str,
    value: dict,
    encode: bool = True,
    host: str = config.host,
) -> dict:
    """Update the value of a specific Submodel.

    Args:
        submodel_id: The unique identifier of the Submodel.
        value: A dictionary representing the updated Submodel value.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the updated Submodel value.

    Raises:
        HTTPError: If the PATCH request fails.
    """
    with Client(host=host) as client:
        return client.update_submodel_value(submodel_id, value, encode)


def get_submodel_metadata(
    submodel_id: str,
    encode: bool = True,
    host: str = config.host,
) -> dict:
    """Retrieve the metadata of a specific Submodel.

    Args:
        submodel_id: The unique identifier of the Submodel.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A dictionary representing the Submodel metadata.

    Raises:
        HTTPError: If the GET request fails.
    """
    with Client(host=host) as client:
        return client.get_submodel_metadata(submodel_id, encode)


# ─────────────────────────────── Sync Submodel Elements ───────────────────────────────


def get_submodel_elements(
    submodel_id: str,
    encode: bool = True,
    host: str = config.host,
) -> dict:
    """Retrieve all Submodel elements from a specific Submodel.

    Args:
        submodel_id: The unique identifier of the Submodel.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Returns:
        A list of dictionaries representing the Submodel elements.

    Raises:
        HTTPError: If the GET request fails.
    """
    with Client(host=host) as client:
        return client.get_submodel_elements(submodel_id, encode)


def create_submodel_element(
    submodel_id: str,
    element: dict,
    id_short_path: str | None = None,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Create a Submodel element.

    Args:
        submodel_id: The unique identifier of the Submodel.
        element: A dictionary representing the Submodel element to create.
        id_short_path: The idShort path for the new Submodel element.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the POST request fails.
    """
    with Client(host=host) as client:
        client.create_submodel_element(submodel_id, element, id_short_path, encode)


def get_submodel_element(
    submodel_id: str,
    id_short_path: str,
    encode: bool = True,
    host: str = config.host,
) -> dict:
    """Retrieve a specific Submodel element by its idShort path.

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
    with Client(host=host) as client:
        return client.get_submodel_element(submodel_id, id_short_path, encode)


def update_submodel_element(
    submodel_id: str,
    id_short_path: str,
    element: dict,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Update or create a Submodel element by full replacement.

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
        element: A dictionary representing the new element content.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the PUT request fails.
    """
    with Client(host=host) as client:
        client.update_submodel_element(submodel_id, id_short_path, element, encode)


def delete_submodel_element(
    submodel_id: str,
    id_short_path: str,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Delete a specific Submodel element by its idShort path.

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the DELETE request fails.
    """
    with Client(host=host) as client:
        client.delete_submodel_element(submodel_id, id_short_path, encode)


def get_submodel_element_value(
    submodel_id: str,
    id_short_path: str,
    encode: bool = True,
    host: str = config.host,
) -> JSON:
    """Retrieve the raw value of a specific Submodel element.

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
    with Client(host=host) as client:
        return client.get_submodel_element_value(submodel_id, id_short_path, encode)


def update_submodel_element_value(
    submodel_id: str,
    id_short_path: str,
    value: str,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Update the value of a specific Submodel element.

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
        value: The new value to assign to the Submodel element.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: Base URL of the AAS server. Defaults to configured host.

    Raises:
        HTTPError: If the PATCH request fails.
    """
    with Client(host=host) as client:
        client.update_submodel_element_value(submodel_id, id_short_path, value, encode)


# ─────────────────────────────────── Sync Service ─────────────────────────────────────


def get_health_status(host: str = config.host, **kwargs: Any) -> str:
    """Check health status of the AAS environment.

    Args:
        host: Base URL of the AAS server. Defaults to configured host.Args:
        **kwargs: Additional keyword arguments to pass to the request.

    Returns:
        The health status string ('UP', 'DOWN', 'OUT_OF_SERVICE', 'UNKNOWN').

    Raises:
        HTTPError: If the GET request fails.
    """
    with Client(host=host) as client:
        return client.get_health_status(**kwargs)


def is_healthy(host: str = config.host, **kwargs: Any) -> bool:
    """Check if the AAS environment is ready for requests.

    Args:
        host: Base URL of the AAS server. Defaults to configured host.Args:
        **kwargs: Additional keyword arguments to pass to the request.

    Returns:
        True if the environment is healthy (status == 'UP'), False otherwise.
    """
    with Client(host=host) as client:
        return client.is_healthy(**kwargs)
