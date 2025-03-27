from typing import Any

from neo4j import Driver, GraphDatabase

from shellsmith.config import config

_driver: Driver | None = None


def get_driver() -> Driver:
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(config.neo4j_uri, auth=None)
    return _driver


def close_driver() -> None:
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


##################
# Shells
##################


def get_shells() -> list[dict[str, Any]]:
    query = """
    MATCH (shell:AssetAdministrationShell)
    RETURN shell;
    """
    with get_driver().session() as session:
        result = session.run(query)
        shells = [dict(record["shell"]) for record in result]
        return shells


def get_shell(shell_id: str) -> dict[str, Any] | None:
    query = """
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
    query = """
    MATCH (submodel:Submodel)
    RETURN submodel
    """
    with get_driver().session() as session:
        result = session.run(query)
        submodels = [dict(record["submodel"]) for record in result]
        return submodels


def get_submodel(submodel_id: str) -> dict[str, Any]:
    query = """
    MATCH (submodel:Submodel {id: $submodel_id})
    RETURN submodel
    """
    with get_driver().session() as session:
        result = session.run(query, submodel_id=submodel_id)
        record = result.single()
        return dict(record["submodel"]) if record else None


def get_submodel_elements(submodel_id: str) -> list[dict[str, Any]]:
    query = """
    MATCH (sme:SubmodelElement {smId: $submodel_id})
    RETURN sme;
    """
    with get_driver().session() as session:
        result = session.run(query, submodel_id=submodel_id)
        return [dict(record["sme"]) for record in result]


def get_submodel_element(submodel_id: str, id_short_path: str) -> dict[str, Any] | None:
    query = """
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
    """
    Dangerous!
    Deletes all nodes and relationships in the graph.
    """
    query = """
    MATCH (n)
    DETACH DELETE n;
    """
    with get_driver().session() as session:
        session.run(query)
