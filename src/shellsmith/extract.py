"""Extraction utilities for working with AAS Shells and Submodels."""


def collect_submodel_ids(shell: dict) -> list[str]:
    """Extracts submodel references from the given shell.

    Args:
        shell: A dictionary representing the shell.

    Returns:
        A list of submodel IDs referenced by the shell.
    """
    return [submodel["keys"][0]["value"] for submodel in shell.get("submodels", [])]
