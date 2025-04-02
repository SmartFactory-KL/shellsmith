from shellsmith import crud
from shellsmith.cli.formats import OutputFormat
from shellsmith.cli.pretty import print_data
from shellsmith.cli.simplify import enrich, simplify_many


def test_print_shells_output_simple():
    shells = crud.get_shells()
    simplified = simplify_many(shells)
    enriched = [enrich(shell) for shell in simplified]
    print_data(enriched, output_format=OutputFormat.SIMPLE, title="Shells")


def test_print_shells_output_tree():
    shells = crud.get_shells()
    print_data(shells, output_format=OutputFormat.TREE, title="Shells")


def test_print_submodels_output_simple():
    submodels = crud.get_submodels()
    simplified = simplify_many(submodels)
    print_data(simplified, output_format=OutputFormat.SIMPLE, title="Submodels")


def test_print_submodels_output_tree():
    submodels = crud.get_submodels()
    print_data(submodels, output_format=OutputFormat.TREE, title="Submodels")
