import requests

from shellsmith import __version__, services
from shellsmith.config import config

from .commands import (
    info,
    nuke,
    shell_delete,
    submodel_delete,
    submodel_element_get,
    submodel_element_patch,
    upload,
)
from .parser import build_parser
from ..utils import base64_decode, base64_encode


def print_header():
    print("===============================================")
    print(f" Shellsmith - AAS Toolkit v{__version__}")
    print(f" Host: {config.host} ({services.health()})")
    print("===============================================")
    print()


def main():
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "upload": lambda _args: upload(args.path),
        "info": lambda _args: info(),
        "nuke": lambda _args: nuke(),
        "shell.delete": lambda _args: shell_delete(args.id, cascade=args.cascade),
        "submodel.delete": lambda _args: submodel_delete(args.id, unlink=args.unlink),
        "sme.get": lambda _args: submodel_element_get(args.id, args.path),
        "sme.patch": lambda _args: submodel_element_patch(
            args.id, args.path, args.value
        ),
        "encode": lambda _args: print(base64_encode(args.id)),
        "decode": lambda _args: print(base64_decode(args.value)),
    }

    try:
        key = args.command
        if key == "shell" and args.shell_command:
            key += f".{args.shell_command}"
        elif key == "submodel" and args.submodel_command:
            key += f".{args.submodel_command}"
        elif key == "sme" and args.submodel_element_command:
            key += f".{args.submodel_element_command}"

        handler = commands.get(key)
        if handler:
            if key not in ("encode", "decode"):
                print_header()
            handler(args)
        else:
            parser.print_help()
    except requests.exceptions.ConnectionError as e:
        print(f"😩 Cannot reach {config.host}: {e}")
