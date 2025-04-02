"""Defines supported output formats for CLI commands."""

from enum import Enum


class OutputFormat(str, Enum):
    """Supported output formats for CLI commands."""

    SIMPLE = "simple"
    JSON = "json"
    TREE = "tree"
    YAML = "yaml"
    PLAIN = "plain"
