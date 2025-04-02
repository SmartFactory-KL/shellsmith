"""Module for interacting with the Neo4j database."""

from functools import cache
from typing import Any

from neo4j import Driver, GraphDatabase
from typing_extensions import LiteralString

from shellsmith.config import config


@cache
def get_driver() -> Driver:
    """Returns a cached Neo4j driver instance.

    Establishes and caches a Neo4j driver to avoid reinitialization.

    Returns:
        The Neo4j driver instance.
    """
    return GraphDatabase.driver(config.neo4j_uri, auth=None)


def close_driver() -> None:
    """Closes the active Neo4j driver and clears the cache."""
    driver = get_driver()
    driver.close()
    get_driver.cache_clear()


##################
# Shells
##################


def get_shells() -> list[dict[str, Any]]:
    """Retrieves all Asset Administration Shells from the database.

    Returns:
        A list of dictionaries representing all shells in the database.
    """
    query: LiteralString = """
    MATCH (shell:AssetAdministrationShell)
    RETURN shell;
    """
    with get_driver().session() as session:
        result = session.run(query)
        shells = [dict(record["shell"]) for record in result]
        return shells


def get_shell(shell_id: str) -> dict[str, Any] | None:
    """Retrieves a specific shell by its ID.

    Args:
        shell_id: The unique identifier of the shell.

    Returns:
        A dictionary representing the shell, or None if not found.
    """
    query: LiteralString = """
    MATCH (shell:AssetAdministrationShell {id: $shell_id})
    RETURN shell;
    """
    with get_driver().session() as session:
        result = session.run(query, shell_id=shell_id)
        record = result.single()
        return dict(record["shell"]) if record else None


##################
# Submodels
##################


def get_submodels() -> list[dict[str, Any]]:
    """Retrieves all submodels from the database.

    Returns:
        A list of dictionaries representing all submodels in the database.
    """
    query: LiteralString = """
    MATCH (submodel:Submodel)
    RETURN submodel
    """
    with get_driver().session() as session:
        result = session.run(query)
        submodels = [dict(record["submodel"]) for record in result]
        return submodels


def get_submodel(submodel_id: str) -> dict[str, Any]:
    """Retrieves a specific submodel by its ID.

    Args:
        submodel_id: The unique identifier of the submodel.

    Returns:
        A dictionary representing the submodel, or None if not found.
    """
    query: LiteralString = """
    MATCH (submodel:Submodel {id: $submodel_id})
    RETURN submodel
    """
    with get_driver().session() as session:
        result = session.run(query, submodel_id=submodel_id)
        record = result.single()
        return dict(record["submodel"]) if record else None


def get_submodel_elements(submodel_id: str) -> list[dict[str, Any]]:
    """Retrieves all submodel elements for a specific submodel.

    Args:
        submodel_id: The unique identifier of the submodel.

    Returns:
        A list of dictionaries representing submodel elements.
    """
    query: LiteralString = """
    MATCH (sme:SubmodelElement {smId: $submodel_id})
    RETURN sme;
    """
    with get_driver().session() as session:
        result = session.run(query, submodel_id=submodel_id)
        return [dict(record["sme"]) for record in result]


def get_submodel_element(submodel_id: str, id_short_path: str) -> dict[str, Any] | None:
    """Retrieves a specific submodel element by submodel ID and idShortPath.

    Args:
        submodel_id: The unique identifier of the submodel.
        id_short_path: The idShortPath of the submodel element.

    Returns:
        A dictionary representing the submodel element, or None if not found.
    """
    query: LiteralString = """
    MATCH (sme:SubmodelElement {smId: $submodel_id, idShortPath: $id_short_path})
    RETURN sme;
    """
    with get_driver().session() as session:
        result = session.run(
            query,
            submodel_id=submodel_id,
            id_short_path=id_short_path,
        )
        record = result.single()
        return dict(record["sme"]) if record else None


def detach_delete_all() -> None:
    """Deletes all nodes and relationships from the Neo4j database.

    This performs a full reset of the graph by removing all nodes and edges.
    """
    query: LiteralString = """
    MATCH (n)
    DETACH DELETE n;
    """
    with get_driver().session() as session:
        session.run(query)
