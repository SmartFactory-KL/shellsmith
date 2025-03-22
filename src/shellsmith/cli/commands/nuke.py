from shellsmith import services


def nuke():
    print("☣️ Deleting all Shells and Submodels!")
    print("☢️ Deleting all Shells and Submodels!")
    print("⚠️ Deleting all Shells and Submodels!")
    services.delete_all_shells()
    services.delete_all_submodels()
