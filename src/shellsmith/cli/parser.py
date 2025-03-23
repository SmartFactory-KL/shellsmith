import argparse
from pathlib import Path

from shellsmith import __version__


def build_parser():
    parser = argparse.ArgumentParser(description="AAS Tools CLI")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ──────────────────────────── upload ────────────────────────────
    upload_parser = subparsers.add_parser("upload", help="Upload AAS file or folder")
    upload_parser.add_argument("path", type=Path, help="Path to the AAS file or folder")

    # ───────────────────────────── info ─────────────────────────────
    subparsers.add_parser("info", help="Display all AAS shells and their submodels")

    # ───────────────────────────── nuke ─────────────────────────────
    subparsers.add_parser("nuke", help="Delete all AAS shells and submodels")

    # ──────────────────────────── shell ─────────────────────────────
    shell_parser = subparsers.add_parser(
        "shell",
        help="Manage Asset Administration Shells",
    )
    shell_subparsers = shell_parser.add_subparsers(dest="shell_command")
    shell_delete_parser = shell_subparsers.add_parser(
        "delete",
        help="Delete an AAS Shell by ID",
    )
    shell_delete_parser.add_argument("id", type=str, help="ID of the shell to delete")
    shell_delete_parser.add_argument(
        "--cascade",
        "-c",
        action="store_true",
        help="Also delete all referenced submodels",
    )

    # ───────────────────────────── submodel ─────────────────────────────
    submodel_parser = subparsers.add_parser("submodel", help="Manage Submodels")
    submodel_subparsers = submodel_parser.add_subparsers(dest="submodel_command")
    submodel_delete_parser = submodel_subparsers.add_parser(
        "delete",
        help="Delete a Submodel by ID",
    )
    submodel_delete_parser.add_argument(
        "id",
        type=str,
        help="ID of the submodel to delete",
    )
    submodel_delete_parser.add_argument(
        "--unlink",
        "-u",
        action="store_true",
        help="Remove all Shell references to this Submodel",
    )

    # ───────────────────────────── encode ─────────────────────────────
    encode_parser = subparsers.add_parser("encode", help="Encode a string to base64")
    encode_parser.add_argument("id", type=str, help="Text to encode")

    # ───────────────────────────── decode ─────────────────────────────
    decode_parser = subparsers.add_parser("decode", help="Decode a base64 string")
    decode_parser.add_argument("value", type=str, help="Base64 string to decode")

    return parser
