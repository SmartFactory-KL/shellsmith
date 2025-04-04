"""Shell CRUD operations for AAS environments."""

import requests

from shellsmith.config import DEFAULT_TIMEOUT, config
from shellsmith.utils import base64_encoded


def get_shells(host: str = config.host) -> list[dict]:
    """Retrieves all Shells from the AAS server.

    Corresponds to:
    GET /shells

    Args:
        host: The base URL of the AAS server. Defaults to the configured host.

    Returns:
        A list of dictionaries representing the Shells.

    Raises:
        HTTPError: If the GET request fails.
    """
    url = f"{host}/shells"
    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    json_response = response.json()
    shells = json_response["result"]
    return shells


def post_shell(shell: dict, host: str = config.host) -> dict:
    """Creates a new Shell on the AAS server.

    Corresponds to:
    POST /shells

    Args:
        shell: A dictionary representing the Shell to be created.
        host: The base URL of the AAS server. Defaults to the configured host.

    Returns:
        A dictionary representing the created Shell.

    Raises:
        HTTPError: If the POST request fails.
    """
    url = f"{host}/shells"
    response = requests.post(url, json=shell, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_shell(shell_id: str, encode: bool = True, host: str = config.host) -> dict:
    """Retrieves a specific Shell by its ID.

    Corresponds to:
    GET /shells/{shell_id}

    Args:
        shell_id: The unique identifier of the Shell.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Returns:
        A dictionary representing the Shell.

    Raises:
        HTTPError: If the GET request fails.
    """
    shell_id = base64_encoded(shell_id, encode)
    url = f"{host}/shells/{shell_id}"

    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    shell = response.json()
    return shell


def put_shell(
    shell_id: str, shell: dict, encode: bool = True, host: str = config.host
) -> None:
    """Updates an existing Shell on the AAS server by its ID.

    Corresponds to:
    PUT /shells/{shell_id}

    Args:
        shell_id: The unique identifier of the Shell.
        shell: A dictionary representing the updated Shell content.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Raises:
        HTTPError: If the PUT request fails.
    """
    shell_id = base64_encoded(shell_id, encode)
    url = f"{host}/shells/{shell_id}"
    response = requests.put(url, json=shell, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()


def delete_shell(shell_id: str, encode: bool = True, host: str = config.host) -> None:
    """Deletes a specific Shell by its ID.

    Corresponds to:
    DELETE /shells/{shell_id}

    Args:
        shell_id: The unique identifier of the Shell.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Raises:
        HTTPError: If the DELETE request fails.
    """
    shell_id = base64_encoded(shell_id, encode)

    url = f"{host}/shells/{shell_id}"
    response = requests.delete(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()


def get_submodel_refs(
    shell_id: str,
    encode: bool = True,
    host: str = config.host,
) -> list[dict]:
    """Retrieves all submodel references from a specific Shell.

    Corresponds to:
    GET /shells/{shell_id}/submodel-refs

    Args:
        shell_id: The unique identifier of the Shell.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Returns:
        A list of dictionaries representing the submodel references.

    Raises:
        HTTPError: If the GET request fails.
    """
    shell_id = base64_encoded(shell_id, encode)

    url = f"{host}/shells/{shell_id}/submodel-refs"
    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    submodel_refs = response.json()["result"]
    return submodel_refs


def post_submodel_ref(
    shell_id: str,
    submodel_ref: dict,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Creates a submodel reference for a specific Shell.

    Corresponds to:
    POST /shells/{shell_id}/submodel-refs

    Args:
        shell_id: The unique identifier of the Shell.
        submodel_ref: A dictionary representing the submodel reference to be added.
        encode: Whether to Base64-encode the Shell ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Raises:
        HTTPError: If the POST request fails.
    """
    shell_id = base64_encoded(shell_id, encode)
    url = f"{host}/shells/{shell_id}/submodel-refs"
    response = requests.post(url, json=submodel_ref, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()


def delete_submodel_ref(
    shell_id: str,
    submodel_id: str,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Deletes a specific submodel reference from a Shell.

    Corresponds to:
    DELETE /shells/{shell_id}/submodel-refs/{submodel_id}

    Args:
        shell_id: The unique identifier of the Shell.
        submodel_id: The unique identifier of the submodel.
        encode: Whether to Base64-encode both identifiers. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Raises:
        HTTPError: If the DELETE request fails.
    """
    shell_id = base64_encoded(shell_id, encode)
    submodel_id = base64_encoded(submodel_id, encode)

    url = f"{host}/shells/{shell_id}/submodel-refs/{submodel_id}"
    response = requests.delete(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
