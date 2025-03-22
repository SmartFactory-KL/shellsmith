import base64
from typing import Optional


def base64_encode(text: Optional[str]) -> Optional[str]:
    try:
        return (
            base64.urlsafe_b64encode(text.encode("utf-8"))
            .decode("utf-8")
            .rstrip("=")  # padding character if input long multiple of 3
        )
    except (TypeError, AttributeError) as e:
        if text is None:
            return None
        raise e


def base64_decode(encoded_text: Optional[str]) -> Optional[str]:
    try:
        missing_padding = 4 - (len(encoded_text) % 4)
        if missing_padding > 0:
            encoded_text += "=" * missing_padding
        return base64.urlsafe_b64decode(encoded_text).decode("utf-8")
    except TypeError as e:
        if encoded_text is None:
            return None
        raise e


def base64_encoded(identifier: str, encode: bool) -> str:
    """
    Return the base64-encoded identifier if encode is True;
    otherwise, return it unchanged.
    """
    return base64_encode(identifier) if encode else identifier
