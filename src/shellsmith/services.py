"""Module for interacting with the AAS Environment API."""

import requests

from shellsmith import crud
from shellsmith.config import config
from shellsmith.extract import collect_submodel_ids


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
    shell = crud.get_shell(shell_id)
    if "submodels" not in shell:
        return []

    submodel_ids = collect_submodel_ids(shell)
    submodels: list[dict] = []

    for submodel_id in submodel_ids:
        try:
            submodel = crud.get_submodel(submodel_id)
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
    crud.delete_shell(shell_id, host=host)


def delete_submodels_of_shell(shell_id: str, host: str = config.host) -> None:
    """Deletes all submodels associated with the specified shell.

    Submodels that do not exist are skipped with a warning.

    Args:
        shell_id: The unique identifier of the shell.
        host: The base URL of the AAS server. Defaults to the configured host.
    """
    shell = crud.get_shell(shell_id, host=host)

    if "submodels" in shell:
        for submodel in shell["submodels"]:
            submodel_id = submodel["keys"][0]["value"]
            try:
                crud.delete_submodel(submodel_id, host=host)
            except requests.exceptions.HTTPError:
                print(f"Warning: Submodel {submodel_id} doesn't exist")


def remove_submodel_references(submodel_id: str, host: str = config.host) -> None:
    """Removes all references to a submodel from existing shells.

    Args:
        submodel_id: The unique identifier of the submodel.
        host: The base URL of the AAS server.  Defaults to the configured host.
    """
    shells = crud.get_shells(host=host)
    for shell in shells:
        if submodel_id in collect_submodel_ids(shell):
            crud.delete_submodel_ref(shell["id"], submodel_id)


def remove_dangling_submodel_refs() -> None:
    """Removes all dangling submodel references from existing shells.

    A dangling reference is one that points to a submodel which no longer exists.
    """
    shells = crud.get_shells()
    submodels = crud.get_submodels()
    submodel_ids = {submodel["id"] for submodel in submodels}

    for shell in shells:
        for submodel_id in collect_submodel_ids(shell):
            if submodel_id not in submodel_ids:
                crud.delete_submodel_ref(shell["id"], submodel_id)


def delete_all_submodels(host: str = config.host) -> None:
    """Deletes all submodels from the AAS environment.

    Args:
        host: The base URL of the AAS server. Defaults to the configured host.
    """
    submodels = crud.get_submodels(host=host)
    for submodel in submodels:
        crud.delete_submodel(submodel["id"])


def delete_all_shells(host: str = config.host) -> None:
    """Deletes all shells from the AAS environment.

    Args:
        host: The base URL of the AAS server. Defaults to the configured host.
    """
    shells = crud.get_shells()
    for shell in shells:
        crud.delete_shell(shell["id"], host=host)


def health(timeout: float = 0.1, host: str = config.host) -> str:
    """Checks the health status of the AAS Environment.

    Args:
        timeout: Timeout in seconds for the health check request. Defaults to 0.1.
        host: The base URL of the AAS server. Defaults to the configured host.

    Returns:
        "UP" if the service is reachable, otherwise "DOWN".
    """
    url = f"{host}/actuator/health"

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return data["status"]
    except requests.exceptions.RequestException:
        return "DOWN"


def find_unreferenced_submodels(host: str = config.host) -> list[str]:
    """Finds all submodels not referenced by any shell.

    Returns:
        A list of submodel IDs that are not referenced by any shell.
    """
    shells = crud.get_shells(host)
    submodels = crud.get_submodels(host)

    submodel_ref_ids = {
        submodel_id for shell in shells for submodel_id in collect_submodel_ids(shell)
    }

    submodel_ids = {submodel["id"] for submodel in submodels}
    return list(submodel_ids - submodel_ref_ids)


def find_dangling_submodel_refs(host: str = config.host) -> list[dict]:
    """Finds all dangling submodel references across all shells.

    A dangling reference is a submodel reference that does not resolve to an existing
    submodel.

    Returns:
        A list of simplified shell mappings with missing submodel IDs.
    """
    shells = crud.get_shells(host)
    submodels = crud.get_submodels(host)
    existing_submodel_ids = {submodel["id"] for submodel in submodels}

    dangling_list: list[dict] = []

    for shell in shells:
        missing_refs = [
            submodel_id
            for submodel_id in collect_submodel_ids(shell)
            if submodel_id not in existing_submodel_ids
        ]
        if missing_refs:
            id_short = shell.get("idShort", "<no idShort>")
            submodels = [{"<missing>": submodel_id} for submodel_id in missing_refs]
            entry = {id_short: shell["id"], "submodels": submodels}
            dangling_list.append(entry)

    return dangling_list
