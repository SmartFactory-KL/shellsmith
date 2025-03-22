[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Shellsmith

A Python toolkit and CLI for managing Asset Administration Shells (AAS), Submodels, and related resources.

## 🚀 Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/ptrstn/shellsmith
```

## 🛠️ Usage

```bash
aas --help
```

Common commands:

```bash
aas info                  # Show all shells and submodels
aas upload <file|folder>  # Upload AAS file or folder
aas shell delete <id>     # Delete a shell
aas submodel delete <id>  # Delete a submodel
```

Use `--cascade` or `--unlink` for cleanup options:

```bash
aas shell delete <id> --cascade      # Also delete referenced submodels
aas submodel delete <id> --unlink    # Remove references from shells
```

## ⚙️ Development

```bash
git clone https://github.com/ptrstn/shellsmith
cd shellsmith
python -m venv .venv
source .venv/bin/activate    # or .venv\Scripts\activate on Windows
pip install -e .[test]
```

### ✅ Testing

```bash
pytest --cov
```
