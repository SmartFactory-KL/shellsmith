# Command-Line Interface

**aas-cli** provides a powerful Typer-based command-line interface for interacting with Asset Administration Shells through the Shellsmith ecosystem.

---

## Installation

**aas-cli** is automatically installed when you install Shellsmith with the optional `cli` dependency `shellsmith[cli]`.
You can also install **aas-cli** independently:

```bash
pip install aas-cli
```

---

## Getting Started

<!-- termynal -->

```
$ aas --help
╭─ Commands ──────────────────────────────────────────────────────────────╮
│ upload   Uploads a single AAS file or all AAS files from a folder. │
│ info     Displays the current Shell tree and issues.               │
│ nuke     Deletes all AAS Shells and Submodels.                     │
│ encode   Encodes a value to Base64.                                │
│ decode   Decodes a Base64 value.                                   │
│ get      Get Shells, Submodels and Submodel Elements.              │
│ delete   Delete Shells, Submodels and Submodel elements.           │
│ update   Update Shells, Submodels and Submodel elements.           │
│ create   Create Shells, Submodels and Submodel elements.           │
╰──────────────────────────────────────────────────────────────────────────╯
```

## Top-Level Commands

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

!!! note  
    Use `aas <command> --help` to explore subcommands and options.

---

## Get Commands

| Command                  | Description                                 |
|--------------------------|---------------------------------------------|
| `aas get shells`         | 🔹 Get all available Shells.                |
| `aas get shell`          | 🔹 Get a specific Shell by ID.              |
| `aas get submodel-refs`  | 🔹 Get all Submodel References of a Shell.  |
| `aas get submodels`      | 🔸 Get all Submodels.                       |
| `aas get submodel`       | 🔸 Get a specific Submodel by ID.           |
| `aas get submodel-value` | 🔸 Get the `$value` of a Submodel.          |
| `aas get submodel-meta`  | 🔸 Get the `$metadata` of a Submodel.       |
| `aas get elements`       | 🔻 Get all Submodel Elements of a Submodel. |
| `aas get element`        | 🔻 Get a specific Submodel Element.         |
| `aas get element-value`  | 🔻 Get the `$value` of a Submodel Element.  |

---

## Create Commands

| Command                   | Description                             |
|---------------------------|-----------------------------------------|
| `aas create shell`        | 🔹 Create a new Shell.                  |
| `aas create submodel-ref` | 🔹 Add a Submodel Reference to a Shell. |
| `aas create submodel`     | 🔸 Create a new Submodel.               |
| `aas create element`      | 🔻 Create a new Submodel Element.       |
| `aas create element`      | 🔻 Create an Element at a nested path.  |

!!! note  
    Use either `--data` or `--file`, not both.

---

## Update Commands

| Command                     | Description                                                    |
|-----------------------------|----------------------------------------------------------------|
| `aas update shell`          | 🔹 Update a Shell (full replacement).                          |
| `aas update submodel`       | 🔸 Update a Submodel (full replacement).                       |
| `aas update submodel-value` | 🔸 Update the `$value` of a Submodel (partial update).         |
| `aas update element`        | 🔻 Update a Submodel Element (full replacement).               |
| `aas update element-value`  | 🔻 Update the `$value` of a Submodel Element (partial update). |

---

## Delete Commands

| Command                    | Description                                                    |
|----------------------------|----------------------------------------------------------------|
| `aas delete shell`         | 🔹 Delete a Shell and optionally all referenced Submodels.     |
| `aas delete submodel-ref ` | 🔹 Remove a Submodel reference from a Shell.                   |
| `aas delete submodel`      | 🔸 Delete a Submodel and optionally unlink it from all Shells. |
| `aas delete element`       | 🔻 Delete a Submodel Element.                                  |
