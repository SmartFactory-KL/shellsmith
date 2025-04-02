"""Utility to generate formatted section headers for the CLI."""

import sys

TOTAL_WIDTH = 88
CHAR = "─"


def section(title: str) -> str:
    """Creates a formatted section header for organizing code in a Python file."""
    title = title.strip()
    prefix = "# "
    padding = TOTAL_WIDTH - len(prefix) - len(title) - 2  # 2 spaces around title
    if padding < 0:
        return f"{prefix}{title}"
    pad_left = padding // 2 - len(prefix)
    pad_right = padding - pad_left
    return f"{prefix}{CHAR * pad_left} {title} {CHAR * pad_right}"


if __name__ == "__main__":
    NUM_ARGS = 2
    if len(sys.argv) != NUM_ARGS:
        print('Usage: python section.py "Your Section Title"')
        sys.exit(1)

    print(section(sys.argv[1]))
