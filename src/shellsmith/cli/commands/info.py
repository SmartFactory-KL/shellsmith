from shellsmith import crud, services


def info():
    print("ℹ️ Showing all shells")
    print_shells_tree()
    print_unreferenced_submodels()


def print_unreferenced_submodels():
    submodel_ids = services.find_unreferenced_submodels()

    if submodel_ids:
        print()
        print("⚠️ Unreferenced Submodels:")
        for submodel_id in submodel_ids:
            submodel = crud.get_submodel(submodel_id)
            id_short = submodel["idShort"]
            print(f"- {id_short} ({submodel_id})")


def print_shells_tree():
    shells = crud.get_shells()
    for shell in shells:
        print(f"{shell['idShort']}: {shell['id']}")

        submodels = services.get_shell_submodels(shell["id"])

        for i, submodel in enumerate(submodels):
            is_last = i == len(submodels) - 1
            prefix = "└──" if is_last else "├──"
            print(f"{prefix} {submodel['idShort']}: {submodel['id']}")
