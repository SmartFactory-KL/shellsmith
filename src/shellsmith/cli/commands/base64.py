from shellsmith.utils import base64_decode, base64_encode


def encode(identifier: str):
    return base64_encode(identifier)


def decode(identifier: str):
    return base64_decode(identifier)
