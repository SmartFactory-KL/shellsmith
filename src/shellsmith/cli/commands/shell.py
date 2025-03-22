import requests.exceptions

from shellsmith import crud, services


def shell_delete(shell_id: str, cascade: bool = False):
    print(f"🗑️ Deleting Shell: {shell_id}")
    try:
        if cascade:
            services.delete_shell_cascading(shell_id)
            print(f"✅ Shell '{shell_id}' and its submodels deleted.")
        else:
            crud.delete_shell(shell_id)
            print(f"✅ Shell '{shell_id}' deleted.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ Failed to delete Shell '{shell_id}': {e}")
