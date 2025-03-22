import sys
from unittest.mock import patch

import requests

from shellsmith.cli.main import main
import pytest


def test_main_info(capsys):
    with patch("sys.argv", ["aas", "info"]):
        main()
    out = capsys.readouterr().out
    assert "Shell" in out or "Submodels" in out


def test_main_upload(capsys):
    with patch("sys.argv", ["aas", "upload", "aas"]):
        main()
    captured = capsys.readouterr()
    assert "Uploading" in captured.out


def test_main_shell_delete(semitrailer):
    with patch("sys.argv", ["aas", "shell", "delete", "some-id"]):
        main()


def test_main_submodel_delete_with_unlink(workpiece_carrier_a1):
    with patch("sys.argv", ["aas", "submodel", "delete", "some-id", "--unlink"]):
        main()


def test_main_invalid_command(capsys):
    with patch("sys.argv", ["aas", "unknown"]):
        with pytest.raises(SystemExit):
            main()
    captured = capsys.readouterr()
    assert "usage" in captured.err


def test_main_no_command(capsys):
    with patch("sys.argv", ["aas"]):
        main()
    captured = capsys.readouterr()
    assert "usage" in captured.out


def test_main_connection_error(capsys):
    with patch(
        "requests.get",
        side_effect=requests.exceptions.ConnectionError("Mocked connection error"),
    ):
        with patch.object(sys, "argv", ["aas", "info"]):
            main()

    captured = capsys.readouterr()
    assert "Cannot reach" in captured.out
    assert "Mocked connection error" in captured.out
