"""Module for interacting with the AAS Environment API."""

import requests

import shellsmith
from shellsmith.config import config


def get_shell_submodels(shell_id: str) -> list[dict]:
    """Retrieves all submodels associated with the specified shell.

    For each referenced submodel, this function attempts to fetch its full data.
    Submodels that cannot be retrieved are skipped with a warning.

    Args:
        shell_id: The unique identifier of the shell.

    Returns:
        A list of dictionaries representing the submodels associated with the shell.

    Raises:
        HTTPError: If the shell itself cannot be fetched.
    """
    shell = shellsmith.get_shell(shell_id)
    if "submodels" not in shell:
        return []

    submodel_ids = extract_shell_submodel_refs(shell)
    submodels: list[dict] = []

    for submodel_id in submodel_ids:
        try:
            submodel = shellsmith.get_submodel(submodel_id)
            submodels.append(submodel)
        except requests.exceptions.HTTPError:
            print(f"⚠️  Submodel '{submodel_id}' not found")

    return submodels


def delete_shell_cascading(
    shell_id: str,
    host: str = config.host,
) -> None:
    """Deletes a shell and all its associated submodels.

    Args:
        shell_id: The unique identifier of the shell.
        host: The base URL of the AAS server. Defaults to the configured host.
    """
    delete_submodels_of_shell(shell_id, host=host)
    shellsmith.delete_shell(shell_id, host=host)


def delete_submodels_of_shell(
    shell_id: str,
    host: str = config.host,
) -> None:
    """Deletes all submodels associated with the specified shell.

    Submodels that do not exist are skipped with a warning.

    Args:
        shell_id: The unique identifier of the shell.
        host: The base URL of the AAS server. Defaults to the configured host.
    """
    shell = shellsmith.get_shell(shell_id, host=host)

    if "submodels" in shell:
        for submodel in shell["submodels"]:
            submodel_id = submodel["keys"][0]["value"]
            try:
                shellsmith.delete_submodel(submodel_id, host=host)
            except requests.exceptions.HTTPError:
                print(f"Warning: Submodel {submodel_id} doesn't exist")


def remove_submodel_references(submodel_id: str) -> None:
    """Removes all references to a submodel from existing shells.

    Args:
        submodel_id: The unique identifier of the submodel.
    """
    shells = shellsmith.get_shells()
    for shell in shells:
        if submodel_id in extract_shell_submodel_refs(shell):
            shellsmith.delete_submodel_ref(shell["id"], submodel_id)


def remove_dangling_submodel_refs() -> None:
    """Removes all dangling submodel references from existing shells.

    A dangling reference is one that points to a submodel which no longer exists.
    """
    shells = shellsmith.get_shells()
    submodels = shellsmith.get_submodels()
    submodel_ids = {submodel["id"] for submodel in submodels}

    for shell in shells:
        for submodel_id in extract_shell_submodel_refs(shell):
            if submodel_id not in submodel_ids:
                shellsmith.delete_submodel_ref(shell["id"], submodel_id)


def delete_all_submodels(host: str = config.host) -> None:
    """Deletes all submodels from the AAS environment.

    Args:
        host: The base URL of the AAS server. Defaults to the configured host.
    """
    submodels = shellsmith.get_submodels(host=host)
    for submodel in submodels:
        shellsmith.delete_submodel(submodel["id"])


def delete_all_shells(host: str = config.host) -> None:
    """Deletes all shells from the AAS environment.

    Args:
        host: The base URL of the AAS server. Defaults to the configured host.
    """
    shells = shellsmith.get_shells()
    for shell in shells:
        shellsmith.delete_shell(shell["id"], host=host)


def health(timeout: float = 0.1) -> str:
    """Checks the health status of the AAS Environment.

    Args:
        timeout: Timeout in seconds for the health check request. Defaults to 0.1.

    Returns:
        "UP" if the service is reachable, otherwise "DOWN".
    """
    url = f"{config.host}/actuator/health"

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return data["status"]
    except requests.exceptions.ConnectionError:
        return "DOWN"


def extract_shell_submodel_refs(shell: dict) -> list[str]:
    """Extracts submodel references from the given shell.

    Args:
        shell: A dictionary representing the shell.

    Returns:
        A list of submodel IDs referenced by the shell.
    """
    return [
        submodel["keys"][0]["value"]
        for submodel in shell["submodels"]
        if "submodels" in shell
    ]


def find_unreferenced_submodels() -> list[str]:
    """Finds all submodels not referenced by any shell.

    Returns:
        A list of submodel IDs that are not referenced by any shell.
    """
    shells = shellsmith.get_shells()
    submodels = shellsmith.get_submodels()

    submodel_ref_ids = {
        submodel_id
        for shell in shells
        for submodel_id in extract_shell_submodel_refs(shell)
    }

    submodel_ids = {submodel["id"] for submodel in submodels}
    return list(submodel_ids - submodel_ref_ids)


def find_dangling_submodel_refs() -> dict[str, list[str]]:
    """Finds all dangling submodel references across all shells.

    A dangling reference is a submodel reference that does not resolve to an existing
    submodel.

    Returns:
        A dictionary mapping shell IDs to lists of missing submodel IDs.
    """
    shells = shellsmith.get_shells()
    submodels = shellsmith.get_submodels()
    existing_submodel_ids = {submodel["id"] for submodel in submodels}

    dangling_refs: dict[str, list[str]] = {}

    for shell in shells:
        shell_id = shell["id"]
        for submodel_id in extract_shell_submodel_refs(shell):
            if submodel_id not in existing_submodel_ids:
                dangling_refs.setdefault(shell_id, []).append(submodel_id)

    return dangling_refs
