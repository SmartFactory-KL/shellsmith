"""Handles submodel element operations via CLI."""

import shellsmith


def submodel_element_get(submodel_id: str, id_short_path: str) -> None:
    """Retrieves and prints a Submodel element's value.

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
    """
    print(f"{submodel_id} -> {id_short_path}:")
    element = shellsmith.get_submodel_element(submodel_id, id_short_path)
    value = element.get("value")
    print(value)


def submodel_element_patch(submodel_id: str, id_short_path: str, value: str) -> None:
    """Updates a Submodel element with a new value.

    Args:
        submodel_id: The unique identifier of the Submodel.
        id_short_path: The idShort path of the Submodel element.
        value: The new value to assign to the element.
    """
    shellsmith.patch_submodel_element_value(submodel_id, id_short_path, value)
    print(f"✅ Updated '{id_short_path}' in Submodel '{submodel_id}'")
