# 🐍 Python API

Shellsmith provides a Python SDK to interact with the [Eclipse BaSyx](https://www.eclipse.org/basyx/) AAS REST API.

---

## 🚀 Quick Start

```python
import shellsmith

# Get all Shells (returns pagination metadata)
response = shellsmith.get_shells()
shells = response["result"]  # Extract the actual shells list

# Fetch a specific Shell by ID
shell = shellsmith.get_shell("https://example.com/shells/my-shell")

# Fetch a specific Submodel by ID  
submodel = shellsmith.get_submodel("https://example.com/submodels/my-submodel")

# Read and update a Submodel Element's value
value = shellsmith.get_submodel_element_value(submodel["id"], "temperature")
shellsmith.update_submodel_element_value(submodel["id"], "temperature", "42.0")
```

### Client-based API (Recommended for advanced usage)

```python
from shellsmith.clients import Client, AsyncClient

# Synchronous client
with Client() as client:
    response = client.get_shells()
    shells = response["result"]
    
# Asynchronous client
async with AsyncClient() as client:
    response = await client.get_shells() 
    shells = response["result"]
    health = await client.get_health_status()
```

> ℹ️ `shell_id` and `submodel_id` are automatically base64-encoded unless you pass `encode=False`.

---

## 📦 Uploading

```python
shellsmith.upload_aas("example.aasx")
shellsmith.upload_aas_folder("my-aas-folder/")
```

---

## 🗑️ Deleting

```python
shellsmith.delete_shell("https://example.com/shells/abc123")
shellsmith.delete_submodel("https://example.com/submodels/def456")
```

---

## 🔗 REST Endpoint Mapping

### 🔹 Shells

| Method | Endpoint                                             | Function              |
|--------|------------------------------------------------------|-----------------------|
| GET    | `/shells`                                            | `get_shells`          |
| POST   | `/shells`                                            | `create_shell`        |
| GET    | `/shells/{aasIdentifier}`                            | `get_shell`           |
| PUT    | `/shells/{aasIdentifier}`                            | `update_shell`        |
| DELETE | `/shells/{aasIdentifier}`                            | `delete_shell`        |
| GET    | `/shells/{aasIdentifier}/submodel-refs`              | `get_submodel_refs`   |
| POST   | `/shells/{aasIdentifier}/submodel-refs`              | `create_submodel_ref` |
| DELETE | `/shells/{aasIdentifier}/submodel-refs/{submodelId}` | `delete_submodel_ref` |

---

### 🔸 Submodels

| Method | Endpoint                            | Function                |
|--------|-------------------------------------|-------------------------|
| GET    | `/submodels`                        | `get_submodels`         |
| POST   | `/submodels`                        | `create_submodel`       |
| GET    | `/submodels/{submodelId}`           | `get_submodel`          |
| PUT    | `/submodels/{submodelId}`           | `update_submodel`       |
| DELETE | `/submodels/{submodelId}`           | `delete_submodel`       |
| GET    | `/submodels/{submodelId}/$value`    | `get_submodel_value`    |
| PATCH  | `/submodels/{submodelId}/$value`    | `update_submodel_value` |
| GET    | `/submodels/{submodelId}/$metadata` | `get_submodel_metadata` |

---

### 🔻 Submodel Elements

| Method | Endpoint                                                               | Function                       |
|--------|------------------------------------------------------------------------|--------------------------------|
| GET    | `/submodels/{submodelId}/submodel-elements`                            | `get_submodel_elements`        |
| POST   | `/submodels/{submodelId}/submodel-elements`                            | `create_submodel_element`      |
| GET    | `/submodels/{submodelId}/submodel-elements/`<br>`{idShortPath}`        | `get_submodel_element`         |
| PUT    | `/submodels/{submodelId}/submodel-elements/`<br>`{idShortPath}`        | `update_submodel_element`      |
| POST   | `/submodels/{submodelId}/submodel-elements/`<br>`{idShortPath}`        | `create_submodel_element`      |
| DELETE | `/submodels/{submodelId}/submodel-elements/`<br>`{idShortPath}`        | `delete_submodel_element`      |
| GET    | `/submodels/{submodelId}/submodel-elements/`<br>`{idShortPath}/$value` | `get_submodel_element_value`   |
| PATCH  | `/submodels/{submodelId}/submodel-elements/`<br>`{idShortPath}/$value` | `update_submodel_element_value`|

---

### 📦 Upload

| Method | Endpoint  | Function                              |
|--------|-----------|---------------------------------------|
| POST   | `/upload` | `upload_aas` <br> `upload_aas_folder` |

> 📁 Upload functions are provided via the `shellsmith.upload` submodule.

---

## 🛠️ Advanced Utilities (`shellsmith.services`)

The `services` module provides high-level operations for bulk management, cleanup, and environment diagnostics.

### 🔁 Submodel Utilities

```python
from shellsmith import services
```

#### `get_shell_submodels(shell_id)`

Returns all submodels associated with a given shell. Skips missing submodels with a warning.

#### `delete_submodels_of_shell(shell_id)`

Deletes all submodels referenced by the given shell.

#### `remove_submodel_references(submodel_id)`

Unlinks the given submodel from all referencing shells.

#### `remove_dangling_submodel_refs()`

Finds and removes all submodel references that point to non-existent submodels.

---

### ☢️ Destructive Helpers

#### `delete_shell_cascading(shell_id)`

Deletes a shell *and* all its associated submodels. Use with caution.

#### `delete_all_shells()`

Deletes all Asset Administration Shells in the environment.

#### `delete_all_submodels()`

Deletes all Submodels in the environment.

---

### 🧹 Cleanup & Diagnostics

#### `find_unreferenced_submodels()`

Returns all submodel IDs that are not referenced by any shell.

#### `find_dangling_submodel_refs()`

Returns all shells with broken submodel references (e.g. pointing to deleted submodels).

#### `health()`

Checks the BaSyx environment health. Returns `"UP"` or `"DOWN"`.

---

## 📚 Reference

- 🔗 [Plattform Industrie 4.0 Swagger Docs](https://app.swaggerhub.com/apis/Plattform_i40/Entire-API-Collection)
