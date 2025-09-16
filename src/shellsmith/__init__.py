"""Module level imports."""

from importlib.metadata import version

__version__ = version("shellsmith")

from .api import (
    create_shell,
    create_submodel,
    create_submodel_element,
    create_submodel_ref,
    delete_shell,
    delete_submodel,
    delete_submodel_element,
    delete_submodel_ref,
    get_health_status,
    get_shell,
    get_shells,
    get_submodel,
    get_submodel_element,
    get_submodel_element_value,
    get_submodel_elements,
    get_submodel_metadata,
    get_submodel_refs,
    get_submodel_value,
    get_submodels,
    is_healthy,
    update_shell,
    update_submodel,
    update_submodel_element,
    update_submodel_element_value,
    update_submodel_value,
)
from .clients import AsyncClient, Client
from .upload import upload_aas, upload_aas_folder

# Aliases for backwards compatibility
post_shell = create_shell
put_shell = update_shell

post_submodel = create_submodel
put_submodel = update_submodel
post_submodel_ref = create_submodel_ref
patch_submodel_value = update_submodel_value

post_submodel_element = create_submodel_element
put_submodel_element = update_submodel_element
patch_submodel_element_value = update_submodel_element_value

health = get_health_status
