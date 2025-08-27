from shellsmith import api
from shellsmith.cli.formats import OutputFormat
from shellsmith.cli.pretty import print_data
from shellsmith.cli.simplify import enrich, simplify_many


def test_print_shells_output_simple():
    shells = api.get_shells()["result"]
    simplified = simplify_many(shells)
    enriched = [enrich(shell) for shell in simplified]
    print_data(enriched, output_format=OutputFormat.SIMPLE, title="Shells")


def test_print_shells_output_tree():
    shells = api.get_shells()["result"]
    print_data(shells, output_format=OutputFormat.TREE, title="Shells")


def test_print_submodels_output_simple():
    submodels = api.get_submodels()["result"]
    simplified = simplify_many(submodels)
    print_data(simplified, output_format=OutputFormat.SIMPLE, title="Submodels")


def test_print_submodels_output_tree():
    submodels = api.get_submodels()["result"]
    print_data(submodels, output_format=OutputFormat.TREE, title="Submodels")
