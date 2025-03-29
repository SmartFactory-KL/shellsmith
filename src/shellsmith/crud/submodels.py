"""Submodel and submodel element CRUD operations for AAS environments."""

from urllib.parse import quote

import requests

from shellsmith.config import config
from shellsmith.utils import base64_encoded


def get_submodels(host: str = config.host) -> list[dict]:
    """Retrieves all Submodels from the AAS server.

    Corresponds to:
    GET /submodels

    Args:
        host: The base URL of the AAS server. Defaults to the configured host.

    Returns:
        A list of dictionaries representing the Submodels.

    Raises:
        HTTPError: If the GET request fails.
    """
    url = f"{host}/submodels"

    response = requests.get(url)
    response.raise_for_status()
    json_response = response.json()
    submodels = json_response["result"]
    return submodels


def get_submodel(
    submodel_id: str, encode: bool = True, host: str = config.host
) -> dict:
    """Retrieves a specific Submodel by its ID.

    Corresponds to:
    GET /submodels/{submodel_id}

    Args:
        submodel_id: The unique identifier of the submodel.
        encode: Whether to Base64-encode the submodel ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Returns:
        A dictionary representing the submodel.

    Raises:
        HTTPError: If the GET request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    url = f"{host}/submodels/{submodel_id}"

    response = requests.get(url)
    response.raise_for_status()
    submodel = response.json()
    return submodel


def delete_submodel(
    submodel_id: str,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Deletes a specific Submodel by its ID.

    Corresponds to:
    DELETE /submodels/{submodel_id}

    Args:
        submodel_id: The unique identifier of the Submodel.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Raises:
        HTTPError: If the DELETE request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    url = f"{host}/submodels/{submodel_id}"

    response = requests.delete(url)
    response.raise_for_status()


# ─────────────────────────── Submodel elements ───────────────────────────


def get_submodel_elements(
    submodel_id: str,
    encode: bool = True,
    host: str = config.host,
) -> list[dict]:
    """Retrieves all Submodel elements from a specific Submodel.

    Corresponds to:
    GET /submodels/{submodel_id}/submodel-elements

    Args:
        submodel_id: The unique identifier of the Submodel.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Returns:
        A list of dictionaries representing the Submodel elements.

    Raises:
        HTTPError: If the GET request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    url = f"{host}/submodels/{submodel_id}/submodel-elements"

    response = requests.get(url)
    response.raise_for_status()
    json_response = response.json()
    elements = json_response["result"]
    return elements


def get_submodel_element(
    submodel_id: str,
    id_short_path: str,
    encode: bool = True,
    host: str = config.host,
) -> dict:
    """Retrieves a specific Submodel element by its idShort path.

    Corresponds to:
    GET /submodels/{submodel_id}/submodel-elements/{id_short_path}

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Returns:
        A dictionary representing the submodel element.

    Raises:
        HTTPError: If the GET request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    url = f"{host}/submodels/{submodel_id}/submodel-elements/{id_short_path}"

    response = requests.get(url)
    response.raise_for_status()
    element = response.json()
    return element


def delete_submodel_element(
    submodel_id: str,
    id_short_path: str,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Deletes a specific Submodel element by its idShort path.

    Corresponds to:
    DELETE /submodels/{submodel_id}/submodel-elements/{idShortPath}

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Raises:
        HTTPError: If the DELETE request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    id_short_path = quote(id_short_path)

    url = f"{host}/submodels/{submodel_id}/submodel-elements/{id_short_path}"
    response = requests.delete(url)
    response.raise_for_status()


def patch_submodel_element_value(
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
        host: The base URL of the AAS server. Defaults to the configured host.

    Raises:
        HTTPError: If the PATCH request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    id_short_path = quote(id_short_path)
    url = f"{host}/submodels/{submodel_id}/submodel-elements/{id_short_path}/$value"

    response = requests.patch(url, json=value)
    response.raise_for_status()
