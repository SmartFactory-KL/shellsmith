"""Simplification utilities for Asset Administration Shell components."""

from requests import HTTPError

from shellsmith import crud
from shellsmith.config import config
from shellsmith.extract import collect_submodel_ids


def simplify(identifiable: dict) -> dict:
    """Reduces a Shell or Submodel to a idShort → id mapping.

    Args:
        identifiable (dict): Shell or Submodel dictionary to be simplified.

    Returns:
        dict: A simplified dictionary containing the `idShort` value as the key, its
            corresponding `id` value, and optionally a "submodels" key with a list of
            collected submodel IDs.
    """
    id_short = identifiable.get("idShort", "<no idShort>")
    simplified = {id_short: identifiable["id"]}

    if "submodels" in identifiable:
        simplified["submodels"] = collect_submodel_ids(identifiable)
    return simplified


def simplify_many(identifiables: list[dict]) -> list[dict]:
    """Simplifies a list of Identifiables (Shells or Submodels)."""
    return [simplify(item) for item in identifiables]


def enrich(simplified_shell: dict, host: str = config.host) -> dict:
    """Replaces submodel IDs in a simplified shell with simplified submodel dicts."""
    enriched = {**simplified_shell}
    submodels = []

    for submodel_id in simplified_shell.get("submodels", []):
        try:
            submodel = crud.get_submodel(submodel_id, host=host)
            submodels.append(simplify(submodel))
        except HTTPError:
            # Option 1: Skip silently
            # continue

            # Option 2: Add placeholder
            submodels.append({"<missing>": submodel_id})

            # Option 3: Log to console (optional)
            # print(f"⚠️  Warning: Submodel not found: {submodel_id}")

    enriched["submodels"] = submodels
    return enriched


def simplify_element(element: dict) -> dict:
    """Simplifies a Submodel Element to a minimal structure."""
    result = {}
    for key in ("modelType", "idShort", "value"):
        if key in element:
            val = element[key]
            if key == "value":
                if isinstance(val, list):
                    result[key] = [
                        simplify_element(v) if isinstance(v, dict) else v for v in val
                    ]
                elif isinstance(val, dict):
                    result[key] = simplify_element(val)
                else:
                    result[key] = val
            else:
                result[key] = val
    return result
