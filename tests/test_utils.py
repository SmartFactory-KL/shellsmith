from pathlib import Path

import pytest

from shellsmith.utils import base64_decode, base64_encode, generate_uuid, load_data


def test_base64_encode():
    text = "https://smartfactory.de/submodels/fcfa2ad7-d27f-4b76-8827-6d48d63f7666"
    expected = "aHR0cHM6Ly9zbWFydGZhY3RvcnkuZGUvc3VibW9kZWxzL2ZjZmEyYWQ3LWQyN2YtNGI3Ni04ODI3LTZkNDhkNjNmNzY2Ng"  # noqa
    encoded = base64_encode(text)
    assert encoded == expected
    assert base64_encode("A") == "QQ"
    assert base64_encode(None) is None


def test_base64_decode():
    text = "aHR0cHM6Ly9zbWFydGZhY3RvcnkuZGUvc2hlbGxzLzNhNGYxNzIzLWZjN2QtNDkwMy1hNjIxLWQ3OWNlOWU0MjQxYw=="  # noqa
    expected = "https://smartfactory.de/shells/3a4f1723-fc7d-4903-a621-d79ce9e4241c"
    decoded = base64_decode(text)
    assert decoded == expected

    assert base64_decode("QQ===") == "A"
    assert base64_decode("QQ==") == "A"
    assert base64_decode("QQ=") == "A"
    assert base64_decode("QQ") == "A"
    assert base64_decode(None) is None
    with pytest.raises(UnicodeDecodeError):
        base64_decode("asdf")


def test_generate_uuid():
    assert generate_uuid()


def test_load_data():
    assert load_data(Path("aas/Semitrailer.json"))
    with pytest.raises(ValueError):
        load_data(Path("aas/WST_A_1.aasx"))
