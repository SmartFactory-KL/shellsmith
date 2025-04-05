<div align="center">
    <img src="docs/images/logo-purple.png" alt="shellsmith" style="max-width: 100%; width: 600px;">
</div>

<div align="center">
  <a href="https://github.com/ptrstn/shellsmith/actions/workflows/test.yaml"><img src="https://github.com/ptrstn/shellsmith/actions/workflows/test.yaml/badge.svg" alt="Test"></a>
  <a href="https://codecov.io/gh/ptrstn/shellsmith"><img src="https://codecov.io/gh/ptrstn/shellsmith/branch/main/graph/badge.svg" alt="codecov"></a>
  <a href="https://pypi.org/project/shellsmith"><img src="https://img.shields.io/pypi/v/shellsmith?color=%2334D058" alt="PyPI - Version"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
</div>

<p align="center">
    <b>Documentation</b>: <a href="https://shellsmith.pages.dev/" target="_blank">https://shellsmith.pages.dev</a>
</p>

**Shellsmith** is a Python SDK and CLI for managing [Asset Administration Shells (AAS)](https://industrialdigitaltwin.org/en/content-hub/aasspecifications), Submodels, and Submodel Elements via the [Eclipse BaSyx](https://www.eclipse.org/basyx/) REST API.  
 
It provides full client-side access to AAS resources with a clean Python interface and a powerful `typer`-based CLI — ideal for scripting, automation, and digital twin integration workflows.

### Features

- 🐍 **Python SDK** for full CRUD access to Shells, Submodels, and Submodel Elements  
- ⚡ **CLI tool** powered by [Typer](https://typer.tiangolo.com/) for fast scripting and automation  
- ⚙️ Simple `.env`-based configuration for flexible environment switching  
- 🔁 Seamless integration with the [Eclipse BaSyx](https://www.eclipse.org/basyx/) Environment REST API  

## 🚀 Installation

```bash
pip install shellsmith
```

**Requires**: Python 3.10+

## 🔧 Configuration

The default AAS environment host is:

```
http://localhost:8081
```

You can override it by setting the `SHELLSMITH_BASYX_ENV_HOST` environment variable, or by creating a `.env` file in the current working directory or your project root.

```bash
SHELLSMITH_BASYX_ENV_HOST=http://your-host:1234
```

## 🧠 CLI Usage

Shellsmith provides a powerful command-line interface:

```bash
aas --help
```

| Command  | Description                                              |
|----------|----------------------------------------------------------|
| `info`   | Display the current Shell tree and identify issues.      |
| `upload` | Upload a single AAS file or all AAS files from a folder. |
| `nuke`   | ☢️ Delete all Shells and Submodels (irrevocable).        |
| `encode` | Encode a value (e.g. Shell ID) to Base64.                |
| `decode` | Decode a Base64-encoded value.                           |
| `get`    | Get Shells, Submodels, and Submodel Elements.            |
| `delete` | Delete Shells, Submodels, or Submodel Elements.          |
| `update` | Update Shells, Submodels, or Submodel Elements.          |
| `create` | Create new Shells, Submodels, or Submodel Elements.      |

> ℹ️ Run `aas <command> --help` to view subcommands and options.

### 🔎 Get Commands

| Command                   | Description                                 |
|---------------------------|---------------------------------------------|
| `aas get shells`          | 🔹 Get all available Shells.                |
| `aas get shell`           | 🔹 Get a specific Shell by ID.              |
| `aas get submodel-refs`   | 🔹 Get all Submodel References of a Shell.  |
| `aas get submodels`       | 🔸 Get all Submodels.                       |
| `aas get submodel `       | 🔸 Get a specific Submodel by ID.           |
| `aas get submodel-value ` | 🔸 Get the `$value` of a Submodel.          |
| `aas get submodel-meta`   | 🔸 Get the `$metadata` of a Submodel.       |
| `aas get elements`        | 🔻 Get all Submodel Elements of a Submodel. |
| `aas get element`         | 🔻 Get a specific Submodel Element.         |
| `aas get element-value`   | 🔻 Get the `$value` of a Submodel Element.  |

### 🛠️ Create Commands

| Command                    | Description                             |
|----------------------------|-----------------------------------------|
| `aas create shell `        | 🔹 Create a new Shell.                  |
| `aas create submodel-ref ` | 🔹 Add a Submodel Reference to a Shell. |
| `aas create submodel`      | 🔸 Create a new Submodel.               |
| `aas create element `      | 🔻 Create a new Submodel Element.       |
| `aas create element`       | 🔻 Create an Element at a nested path.  |

> ℹ️ Input can be passed via `--data "<json>"` or `--file <*.json|*.yaml>`, but **not both**

### 🧬 Update Commands

| Command                      | Description                                                    |
|------------------------------|----------------------------------------------------------------|
| `aas update shell `          | 🔹 Update a Shell (full replacement).                          |
| `aas update submodel`        | 🔸 Update a Submodel (full replacement).                       |
| `aas update submodel-value ` | 🔸 Update the `$value` of a Submodel (partial update).         |
| `aas update element `        | 🔻 Update a Submodel Element (full replacement).               |
| `aas update element-value `  | 🔻 Update the `$value` of a Submodel Element (partial update). |

> ℹ️ All updates are either full replacements (`PUT`) or partial updates (`PATCH`)

### 🧹 Delete Commands

| Command                   | Description                                                    |
|---------------------------|----------------------------------------------------------------|
| `aas delete shell`        | 🔹 Delete a Shell and optionally all referenced Submodels.     |
| `aas delete submodel-ref` | 🔹 Remove a Submodel reference from a Shell.                   |
| `aas delete submodel`     | 🔸 Delete a Submodel and optionally unlink it from all Shells. |
| `aas delete element`      | 🔻 Delete a Submodel Element.                                  |

> ℹ️ You can pass `--cascade` to also remove the Submodels the Shell references

> ℹ️ You can pass `--remove-refs` to also remove all references to that Submodel

## 🐍 Python API Usage

You can also use `shellsmith` as a Python client library to interact with the BaSyx Environment REST API.

```python
import shellsmith

# List all AAS Shells
shells = shellsmith.get_shells()

# Fetch a specific Shell by ID
shell = shellsmith.get_shell("https://example.com/shells/my-shell")

# List Submodels or Submodel References of a Shell
submodels = shellsmith.get_submodels()
refs = shellsmith.get_submodel_refs("https://example.com/shells/my-shell")

# Fetch a specific Submodel
submodel = shellsmith.get_submodel("https://example.com/submodels/my-submodel")

# Read and update a Submodel Element's value
value = shellsmith.get_submodel_element_value(submodel["id"], "temperature")
shellsmith.patch_submodel_element_value(submodel["id"], "temperature", "42.0")

# Upload a single AAS file or an entire folder (.aasx / .json / .xml)
shellsmith.upload_aas("MyAsset.aasx")
shellsmith.upload_aas_folder("aas_folder/")

# Delete a Shell or Submodel by ID
shellsmith.delete_shell("https://example.com/aas/my-asset")
shellsmith.delete_submodel("https://example.com/submodels/my-submodel")
```

> ℹ️ `shell_id` and `submodel_id` are automatically base64-encoded unless you set `encode=False`. This is required by the BaSyx API for identifier-based URLs.

The tables below show the mapping between BaSyx AAS REST API endpoints and the implemented client functions.

> 📚 See [Plattform_i40 API reference](https://app.swaggerhub.com/apis/Plattform_i40/Entire-API-Collection) for endpoint details.

### Shells

| Method | BaSyx Endpoint                                               | `shellsmith` Function |
|--------|--------------------------------------------------------------|-----------------------|
| GET    | `/shells`                                                    | `get_shells`          |
| POST   | `/shells`                                                    | `post_shell`          |
| GET    | `/shells/{aasIdentifier}`                                    | `get_shell`           |
| PUT    | `/shells/{aasIdentifier}`                                    | `put_shell`           |
| DELETE | `/shells/{aasIdentifier}`                                    | `delete_shell`        |
| GET    | `/shells/{aasIdentifier}/submodel-refs`                      | `get_submodel_refs`   |
| POST   | `/shells/{aasIdentifier}/submodel-refs`                      | `post_submodel_ref`   |
| DELETE | `/shells/{aasIdentifier}/submodel-refs/{submodelIdentifier}` | `delete_submodel_ref` |

### Submodels

| Method | BaSyx Endpoint                              | Shellsmith Function     |
|--------|---------------------------------------------|-------------------------|
| GET    | `/submodels`                                | `get_submodels`         |
| POST   | `/submodels`                                | `post_submodel`         |
| GET    | `/submodels/{submodelIdentifier}`           | `get_submodel`          |
| PUT    | `/submodels/{submodelIdentifier}`           | `put_submodel`          |
| DELETE | `/submodels/{submodelIdentifier}`           | `delete_submodel`       |
| GET    | `/submodels/{submodelIdentifier}/$value`    | `get_submodel_value`    |
| PATCH  | `/submodels/{submodelIdentifier}/$value`    | `patch_submodel_value`  |
| GET    | `/submodels/{submodelIdentifier}/$metadata` | `get_submodel_metadata` |

### Submodel Elements

| Method | BaSyx Endpoint                                                           | Shellsmith Function            |
|--------|--------------------------------------------------------------------------|--------------------------------|
| GET    | `/submodels/{submodelIdentifier}/submodel-elements`                      | `get_submodel_elements`        |
| POST   | `/submodels/{submodelIdentifier}/submodel-elements`                      | `post_submodel_element`        |
| GET    | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}`        | `get_submodel_element`         |
| PUT    | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}`        | `put_submodel_element`         |
| POST   | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}`        | `post_submodel_element`        |
| DELETE | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}`        | `delete_submodel_element`      |
| GET    | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$value` | `get_submodel_element_value`   |
| PATCH  | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$value` | `patch_submodel_element_value` |

### Upload

| Method | BaSyx Endpoint | Shellsmith Function                                 |
|--------|----------------|-----------------------------------------------------|
| POST   | `/upload`      | `upload.upload_aas` <br> `upload.upload_aas_folder` |

> ℹ️ Upload functions are available under the `shellsmith.upload` submodule.

## ⚙️ Development

Clone the repository and set up the virtual environment:

```bash
git clone https://github.com/ptrstn/shellsmith
cd shellsmith
python -m venv .venv
source .venv/bin/activate    # or .venv\Scripts\activate on Windows
pip install -e .[test]
```

### ✅ Testing

Start the BaSyx stack (if needed):

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

Then open `htmlcov/index.html` in your web browser to explore which lines are covered and which are missing.

### 🧼 Code Quality

We use [Ruff](https://docs.astral.sh/ruff/) for linting, formatting, and import sorting.

Check code style:

```bash
ruff check
```

Auto-fix issues:

```bash
ruff check --fix
```

Format code:

```bash
ruff format
```

### 📚 Documentation

Serve the docs locally:

```bash
mkdocs serve
```

Then visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to preview.

Build the static site:

```bash
mkdocs build
```

## Resources

- https://github.com/eclipse-basyx/basyx-java-server-sdk
- https://github.com/admin-shell-io/aas-specs-api
- https://app.swaggerhub.com/apis/Plattform_i40/Entire-API-Collection
