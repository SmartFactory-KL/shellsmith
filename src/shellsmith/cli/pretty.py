"""Rendering utilities for formatting CLI output using Rich."""

import yaml
from rich.console import Console
from rich.json import JSON
from rich.syntax import Syntax
from rich.text import Text
from rich.tree import Tree

from shellsmith.cli.formats import OutputFormat

DEFAULT_TITLE = "📦 Data"
PRIORITY_KEYS = ("idShort", "id", "modelType")


def sort_keys_with_priority(d: dict, priority: list[str] = PRIORITY_KEYS) -> list[str]:
    """Sorts the keys of a dictionary based on a given priority."""
    keys = list(d.keys())
    preferred = [k for k in priority if k in keys]
    rest = sorted(k for k in keys if k not in priority)
    return preferred + rest


def format_value(value: str | int | float | bool | None) -> str:
    """Formats a value for pretty printing."""
    if isinstance(value, str):
        return f"[white]{value}[/]"
    if isinstance(value, int | float):
        return f"[yellow]{value}[/]"
    if isinstance(value, bool):
        return f"[green]{value}[/]"
    if value is None:
        return "[dim]null[/]"
    return str(value)


def format_key(key: str, value: dict | list) -> str:
    """Formats a key for pretty printing."""
    if key == "<no idShort>":
        return f"[dark_orange3 reverse]{key}[/]"
    if value:
        return f"[bright_blue]{key}[/]"
    return f"[red reverse]{key}[/]"


def make_label(identifiable: dict) -> str:
    """Creates a label like 'idShort (id)' from an identifiable dictionary."""
    id_ = identifiable.get("id", "<missing id>") or "<empty id>"
    id_short = identifiable.get("idShort", "<missing idShort>") or "<empty idShort>"
    return f"{id_short} ({id_})"


def build_pretty_tree(data: dict | list[dict], tree: Tree) -> None:
    """Builds a pretty tree from a nested dictionary or list."""
    if isinstance(data, dict):
        for key in sort_keys_with_priority(data):
            value = data[key]
            if isinstance(value, dict | list):
                label = format_key(key, value)
                branch = tree.add(label)
                build_pretty_tree(value, branch)
            else:
                tree.add(f"[cyan]{key}[/]: {format_value(value)}")
    elif isinstance(data, list):
        for index, item in enumerate(data):
            branch = tree.add(f"[magenta][{index}][/]")
            build_pretty_tree(item, branch)
    else:
        tree.add(f"[green]{data}[/]")


def build_simple_tree(simplified_data: list[dict], tree: Tree) -> None:
    """Builds a simple tree from a list of simplified data."""
    for identifiable in simplified_data:
        expected_key_count = 2
        assert len(identifiable.keys()) <= expected_key_count, "Data is not simplified"

        id_short, id_ = next(
            (k, v) for k, v in identifiable.items() if k != "submodels"
        )

        if id_short == "<no idShort>":
            id_short_label = "[dark_orange3 reverse]<no idShort>[/]"
        elif id_short == "<empty idShort>":
            id_short_label = "[yellow reverse]<empty idShort>[/]"
        else:
            id_short_label = f"[green]{id_short}[/green]"

        branch = tree.add(f"{id_short_label}: [grey]{id_}[/grey]")

        for submodel in identifiable.get("submodels", []):
            submodel_id_short, submodel_id = next(iter(submodel.items()))
            if submodel_id_short == "<missing>":
                label = f"[red reverse]{submodel_id_short}[/]: [dim]{submodel_id}[/dim]"
            elif submodel_id_short == "<no idShort>":
                label = f"[dark_orange3 reverse]{submodel_id_short}[/]: {submodel_id}"
            else:
                label = f"[cyan]{submodel_id_short}[/cyan]: {submodel_id}"
            branch.add(label)


def print_pretty_tree(data: dict | list[dict], title: str = DEFAULT_TITLE) -> None:
    """Prints a pretty tree from a nested dictionary or list."""
    console = Console()
    tree = Tree(Text(title, style="bold yellow"))
    build_pretty_tree(data, tree)
    console.print(tree)


def print_simple_tree(simplified_data: list[dict], title: str = DEFAULT_TITLE) -> None:
    """Prints a simple tree from a list of simplified data."""
    console = Console()
    tree = Tree(Text(title, style="bold yellow"))
    build_simple_tree(simplified_data, tree)
    console.print(tree)


def print_yaml(data: dict | list[dict]) -> None:
    """Prints a YAML representation of the given data."""
    yaml_str = yaml.dump(data, sort_keys=False, allow_unicode=True)
    syntax = Syntax(yaml_str, "yaml", theme="monokai", line_numbers=False)
    console = Console()
    console.print(syntax)


def print_data(
    data: dict | list[dict],
    output_format: OutputFormat = OutputFormat.PLAIN,
    title: str = DEFAULT_TITLE,
) -> None:
    """Prints data in the specified format: simple, tree, json, yaml, or plain."""
    console = Console()
    if output_format == OutputFormat.SIMPLE:
        print_simple_tree(data, title=title)
    elif output_format == OutputFormat.TREE:
        print_pretty_tree(data, title=title)
    elif output_format == OutputFormat.JSON:
        console.print(JSON.from_data(data))
    elif output_format == OutputFormat.YAML:
        print_yaml(data)
    else:  #  OutputFormat.PLAIN
        console.print(data)
