"""Submodel and submodel element CRUD operations for AAS environments."""

from urllib.parse import quote

import requests

from shellsmith.config import DEFAULT_TIMEOUT, config
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

    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    json_response = response.json()
    submodels = json_response["result"]
    return submodels


def post_submodel(submodel: dict, host: str = config.host) -> dict:
    """Creates a new Submodel on the AAS server.

    Corresponds to:
    POST /submodels

    Args:
        submodel: A dictionary representing the Submodel to be created.
        host: The base URL of the AAS server. Defaults to the configured host.

    Returns:
        A dictionary representing the created Submodel.

    Raises:
        HTTPError: If the POST request fails.
    """
    url = f"{host}/submodels"
    response = requests.post(url, json=submodel, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_submodel(
    submodel_id: str,
    encode: bool = True,
    host: str = config.host,
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

    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    submodel = response.json()
    return submodel


def put_submodel(
    submodel_id: str,
    submodel: dict,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Updates an existing Submodel by its ID.

    Corresponds to:
    PUT /submodels/{submodel_id}

    Args:
        submodel_id: The unique identifier of the Submodel.
        submodel: A dictionary representing the updated Submodel content.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Raises:
        HTTPError: If the PUT request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    url = f"{host}/submodels/{submodel_id}"
    response = requests.put(url, json=submodel, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()


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

    response = requests.delete(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()


def get_submodel_value(
    submodel_id: str,
    encode: bool = True,
    host: str = config.host,
) -> dict:
    """Retrieves the raw value of a specific Submodel.

    Corresponds to:
    GET /submodels/{submodel_id}/$value

    Args:
        submodel_id: The unique identifier of the Submodel.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Returns:
        A dictionary representing the Submodel value.

    Raises:
        HTTPError: If the GET request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    url = f"{host}/submodels/{submodel_id}/$value"
    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


def patch_submodel_value(
    submodel_id: str,
    value: dict,
    encode: bool = True,
    host: str = config.host,
) -> None:
    """Updates the value of a specific Submodel.

    Corresponds to:
    PATCH /submodels/{submodel_id}/$value

    Args:
        submodel_id: The unique identifier of the Submodel.
        value: A dictionary representing the updated Submodel value.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Raises:
        HTTPError: If the PATCH request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    url = f"{host}/submodels/{submodel_id}/$value"
    response = requests.patch(url, json=value, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()


def get_submodel_metadata(
    submodel_id: str,
    encode: bool = True,
    host: str = config.host,
) -> dict:
    """Retrieves the metadata of a specific Submodel.

    Corresponds to:
    GET /submodels/{submodel_id}/$metadata

    Args:
        submodel_id: The unique identifier of the Submodel.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: The base URL of the AAS server. Defaults to the configured host.

    Returns:
        A dictionary representing the Submodel metadata.

    Raises:
        HTTPError: If the GET request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    url = f"{host}/submodels/{submodel_id}/$metadata"
    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


# ─────────────────────────────── Submodel Elements ────────────────────────────────────


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

    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    json_response = response.json()
    elements = json_response["result"]
    return elements


def post_submodel_element(
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
        id_short_path: The idShort path for the new Submodel element.
        element: A dictionary representing the Submodel element to create.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: The base URL of the AAS server.

    Raises:
        HTTPError: If the POST request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    base = f"{host}/submodels/{submodel_id}/submodel-elements"
    url = f"{base}/{quote(id_short_path)}" if id_short_path else base
    response = requests.post(url, json=element, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()


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

    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    element = response.json()
    return element


def put_submodel_element(
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
        host: The base URL of the AAS server.

    Raises:
        HTTPError: If the PUT request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    id_short_path = quote(id_short_path)
    url = f"{host}/submodels/{submodel_id}/submodel-elements/{id_short_path}"
    response = requests.put(url, json=element, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()


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
    response = requests.delete(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()


def get_submodel_element_value(
    submodel_id: str,
    id_short_path: str,
    encode: bool = True,
    host: str = config.host,
) -> dict:
    """Retrieves the raw value of a specific Submodel element.

    Corresponds to:
    GET /submodels/{submodel_id}/submodel-elements/{idShortPath}/$value

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
        encode: Whether to Base64-encode the Submodel ID. Defaults to True.
        host: The base URL of the AAS server.

    Returns:
        A dictionary representing the raw value.

    Raises:
        HTTPError: If the GET request fails.
    """
    submodel_id = base64_encoded(submodel_id, encode)
    id_short_path = quote(id_short_path)
    url = f"{host}/submodels/{submodel_id}/submodel-elements/{id_short_path}/$value"
    response = requests.get(url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


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

    response = requests.patch(url, json=value, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
