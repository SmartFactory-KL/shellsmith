import shellsmith


def submodel_element_get(submodel_id: str, id_short_path: str):
    print(f"{submodel_id} -> {id_short_path}:")
    element = shellsmith.get_submodel_element(submodel_id, id_short_path)
    value = element.get("value")
    print(value)


def submodel_element_patch(submodel_id: str, id_short_path: str, value: str):
    shellsmith.patch_submodel_element_value(submodel_id, id_short_path, value)
    print(f"✅ Updated '{id_short_path}' in Submodel '{submodel_id}'")
