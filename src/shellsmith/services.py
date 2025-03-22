from typing import Dict, List

import requests

from shellsmith import crud
from shellsmith.config import config


def get_shell_submodels(shell_id: str) -> List[Dict]:
    shell = crud.get_shell(shell_id)
    if "submodels" not in shell:
        return []

    submodel_ids = extract_shell_submodel_refs(shell)
    submodels: List[Dict] = []

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
):
    delete_submodels_of_shell(shell_id, host=host)
    crud.delete_shell(shell_id, host=host)


def delete_submodels_of_shell(
    shell_id: str,
    host: str = config.host,
):
    shell = crud.get_shell(shell_id, host=host)

    if "submodels" in shell:
        for submodel in shell["submodels"]:
            submodel_id = submodel["keys"][0]["value"]
            try:
                crud.delete_submodel(submodel_id, host=host)
            except requests.exceptions.HTTPError:
                print(f"Warning: Submodel {submodel_id} doesn't exist")


def remove_submodel_references(submodel_id: str):
    shells = crud.get_shells()
    for shell in shells:
        if submodel_id in extract_shell_submodel_refs(shell):
            crud.delete_submodel_ref(shell["id"], submodel_id)


def remove_dangling_submodel_refs():
    shells = crud.get_shells()
    submodels = crud.get_submodels()
    submodel_ids = {submodel["id"] for submodel in submodels}

    for shell in shells:
        for submodel_id in extract_shell_submodel_refs(shell):
            if submodel_id not in submodel_ids:
                crud.delete_submodel_ref(shell["id"], submodel_id)


def delete_all_submodels(host: str = config.host):
    submodels = crud.get_submodels(host=host)
    for submodel in submodels:
        crud.delete_submodel(submodel["id"])


def delete_all_shells(host: str = config.host):
    shells = crud.get_shells()
    for shell in shells:
        crud.delete_shell(shell["id"], host=host)


def health(timeout: float = 0.1) -> str:
    url = f"{config.host}/actuator/health"

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return data["status"]
    except requests.exceptions.ConnectionError:
        return "DOWN"


def extract_shell_submodel_refs(shell: Dict) -> List[str]:
    return [
        submodel["keys"][0]["value"]
        for submodel in shell["submodels"]
        if "submodels" in shell
    ]


def find_unreferenced_submodels() -> list[str]:
    shells = crud.get_shells()
    submodels = crud.get_submodels()

    submodel_ref_ids = {
        submodel_id
        for shell in shells
        for submodel_id in extract_shell_submodel_refs(shell)
    }

    submodel_ids = {submodel["id"] for submodel in submodels}
    return list(submodel_ids - submodel_ref_ids)
