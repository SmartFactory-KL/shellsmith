<div align="center">
    <img src="https://raw.githubusercontent.com/ptrstn/shellsmith/main/docs/images/logo-purple-500.png" alt="shellsmith">
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

➡️ Full CLI reference: [shellsmith.pages.dev/cli](https://shellsmith.pages.dev/cli)

## 🐍 Python API Usage

You can also use `shellsmith` as a Python client library to interact with the BaSyx Environment REST API.

```python
import shellsmith

# Fetch all AAS Shells
shells = shellsmith.get_shells()

# Fetch a specific Submodel
submodel = shellsmith.get_submodel("https://example.com/submodels/my-submodel")

# Read and update a Submodel Element's value
value = shellsmith.get_submodel_element_value(submodel["id"], "temperature")
shellsmith.patch_submodel_element_value(submodel["id"], "temperature", "42.0")
```

> ℹ️ `shell_id` and `submodel_id` are automatically base64-encoded unless you pass `encode=False`.

➡️ Full Python API reference: [shellsmith.pages.dev/api](https://shellsmith.pages.dev/api)

## 🔧 Configuration

The default AAS environment host is:

```
http://localhost:8081
```

You can override it in several ways:

- Set the environment variable:  
  ```bash
  SHELLSMITH_BASYX_ENV_HOST=https://your-host:1234
  ```

- Create a `.env` file in your project with:  
  ```dotenv
  SHELLSMITH_BASYX_ENV_HOST=https://your-host:1234
  ```

- Use the `--host` option with any CLI command:  
  ```bash
  aas get shells --host https://your-host:1234
  ```

- Pass the `host` parameter in any `shellsmith` Python function:  
  ```python
  shellsmith.get_shells(host="https://your-host:1234")
  ```

> 💡 The `--host` CLI flag and `host=` Python argument **take precedence** over environment variables and `.env`.

## 🤝 Contributing

We welcome contributions!

See the [Contributing Guide](https://shellsmith.pages.dev/contributing/) for setup, testing, and coding standards.

## Resources

- https://github.com/eclipse-basyx/basyx-java-server-sdk
- https://github.com/admin-shell-io/aas-specs-api
- https://app.swaggerhub.com/apis/Plattform_i40/Entire-API-Collection
