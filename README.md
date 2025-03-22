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

Use `--cascade` or `--unlink` to control deletion behavior:

```bash
aas shell delete <id> --cascade      # Also delete referenced submodels
aas submodel delete <id> --unlink    # Remove references from shells
```

## 📡 API Usage

The table below shows the mapping between BaSyx AAS REST API endpoints and the implemented client functions:

### Shells

| Method | BaSyx Endpoint                                               | Shellsmith Function   |
|--------|--------------------------------------------------------------|-----------------------|
| GET    | `/shells`                                                    | `get_shells`          |
| POST   | `/shells`                                                    | ❌                     |
| GET    | `/shells/{aasIdentifier}`                                    | `get_shell`           |
| PUT    | `/shells/{aasIdentifier}`                                    | ❌                     |
| DELETE | `/shells/{aasIdentifier}`                                    | `delete_shell`        |
| GET    | `/shells/{aasIdentifier}/submodel-refs`                      | `get_submodel_refs`   |
| POST   | `/shells/{aasIdentifier}/submodel-refs`                      | ❌                     |
| DELETE | `/shells/{aasIdentifier}/submodel-refs/{submodelIdentifier}` | `delete_submodel_ref` |

### Submodels

| Method | BaSyx Endpoint                              | Shellsmith Function |
|--------|---------------------------------------------|---------------------|
| GET    | `/submodels`                                | `get_submodels`     |
| POST   | `/submodels`                                | ❌                   |
| GET    | `/submodels/{submodelIdentifier}`           | `get_submodel`      |
| PUT    | `/submodels/{submodelIdentifier}`           | ❌                   |
| DELETE | `/submodels/{submodelIdentifier}`           | `delete_submodel`   |
| GET    | `/submodels/{submodelIdentifier}/$value`    | ❌                   |
| PATCH  | `/submodels/{submodelIdentifier}/$value`    | ❌                   |
| GET    | `/submodels/{submodelIdentifier}/$metadata` | ❌                   |

### Submodel Elements

| Method | BaSyx Endpoint                                                           | Shellsmith Function            |
|--------|--------------------------------------------------------------------------|--------------------------------|
| GET    | `/submodels/{submodelIdentifier}/submodel-elements`                      | `get_submodel_elements`        |
| POST   | `/submodels/{submodelIdentifier}/submodel-elements`                      | ❌                              |
| GET    | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}`        | `get_submodel_element`         |
| PUT    | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}`        | ❌                              |
| POST   | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}`        | ❌                              |
| DELETE | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}`        | `delete_submodel_element`      |
| GET    | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$value` | ❌                              |
| PATCH  | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$value` | `patch_submodel_element_value` |

### Upload

| Method | BaSyx Endpoint | Shellsmith Function                                 |
|--------|----------------|-----------------------------------------------------|
| POST   | `/upload`      | `upload.upload_aas` <br> `upload.upload_aas_folder` |


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

## References

- https://github.com/eclipse-basyx/basyx-java-server-sdk
- https://github.com/admin-shell-io/aas-specs-api
- https://app.swaggerhub.com/apis/Plattform_i40/Entire-API-Collection
