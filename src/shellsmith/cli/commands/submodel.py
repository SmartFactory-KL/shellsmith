import requests

import shellsmith
from shellsmith import services


def submodel_delete(submodel_id: str, unlink: bool = False):
    print(f"🗑️ Deleting Submodel: {submodel_id}")
    try:
        shellsmith.delete_submodel(submodel_id)
        print(f"✅ Submodel '{submodel_id}' deleted.")
    except requests.exceptions.HTTPError:
        print(f"❌ Submodel '{submodel_id}' doesn't exist.")
    if unlink:
        services.remove_submodel_references(submodel_id)
        print(f"✅ Removed Shell references to Submodel '{submodel_id}'.")
