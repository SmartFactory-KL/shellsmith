# 🧑‍💻 Development Guide

Set up **Shellsmith** for local development, testing, linting, and documentation.

> Want to propose a fix, improve the CLI, or update the docs? This guide gets you started.

---

## ⚙️ Setup

Follow these steps to set up your development environment:

Clone the repository:

```bash
git clone https://github.com/SmartFactory-KL/shellsmith
```

Navigate into the project folder:

```bash
cd shellsmith
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

=== "Linux / macOS"

    ```bash
    source .venv/bin/activate
    ```

=== "Windows"

    ```powershell
    .venv\Scripts\activate
    ```

Install the package in editable mode with test and documentation dependencies:

```bash
pip install -e .[test,docs]
```

---

## 🚀 Running the App

You can run Shellsmith in two ways:

### Using the `aas` CLI script

```bash
aas --help
```

!!! note  
    The `aas` command is installed when you install the project (e.g. via `pip install -e .`).  
    It's declared in `pyproject.toml`:

    ```toml
    [project.scripts]
    aas = "shellsmith.cli.app:main"
    ```

### Running the module directly

```bash
python -m shellsmith --help
```

!!! note  
    This executes the package’s `__main__.py` entry point.

---

## 🧪 Running Tests

Start the BaSyx test environment (if needed):

```bash
docker compose up -d
```

Run the test suite with coverage:

```bash
pytest --cov
```

Generate an HTML coverage report:

```bash
pytest --cov --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

---

## 🧼 Code Style
We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting, and [mypy](https://mypy-lang.org/) for static type checking:

Check code:

```bash
ruff check
```

??? note "What is being checked?"

    === "Rules"

        Ruff is configured to enforce modern Python code standards:
        
        The following linting rules are enabled:

        - **Type hints** ([`ANN`](https://docs.astral.sh/ruff/rules/#flake8-annotations-ann))
        - **Common bugs** ([`B`](https://docs.astral.sh/ruff/rules/#flake8-bugbear-b))
        - **Comprehension style** ([`C4`](https://docs.astral.sh/ruff/rules/#flake8-comprehensions-c4))
        - **Docstring style** ([`D`](https://docs.astral.sh/ruff/rules/#pydocstyle-d))
        - **PEP8 errors** ([`E`](https://docs.astral.sh/ruff/rules/#error-e)) and **warnings** ([`W`](https://docs.astral.sh/ruff/rules/#warning-w))
        - **Unused/undefined code** ([`F`](https://docs.astral.sh/ruff/rules/#pyflakes-f))
        - **Imports** ([`I`](https://docs.astral.sh/ruff/rules/#isort-i))
        - **Naming conventions** ([`N`](https://docs.astral.sh/ruff/rules/#pep8-naming-n))
        - **Pylint compatibility** ([`PL`](https://docs.astral.sh/ruff/rules/#pylint-pl))
        - **Simplifications** ([`SIM`](https://docs.astral.sh/ruff/rules/#flake8-simplify-sim))
        - **Modernization** ([`UP`](https://docs.astral.sh/ruff/rules/#pyupgrade-up))
        
        Additional rules and ignores are set in `pyproject.toml`.

    === "pyproject.toml"

        ```toml
        [tool.ruff]
        target-version = "py310"
        
        [tool.ruff.lint]
        select = [
            "ANN",  # flake8-annotations
            "B",    # flake8-bugbear
            "C4",   # flake8-comprehensions
            "D",    # pydocstyle
            "E",    # pycodestyle errors
            "F",    # pyflakes
            "I",    # isort
            "N",    # pep8-naming
            "PL",   # pylint
            "SIM",  # flake8-simplify
            "UP",   # pyupgrade
            "W",    # pycodestyle warnings
        ]
        
        [tool.ruff.lint.pydocstyle]
        convention = "google"
        ```

Auto-fix issues:

```bash
ruff check --fix
```

Format code:

```bash
ruff format
```

Run static type checks:

```bash
mypy src
```

---

## 📚 Docs

We use [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) for documentation.

Serve the documentation locally:

```bash
mkdocs serve
```

!!! note  
    Documentation lives in the `docs/` folder and uses Markdown with Material features.

Then open [http://localhost:8000](http://localhost:8000)

Build the static site:

```bash
mkdocs build
```
