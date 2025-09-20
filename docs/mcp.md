<div style="margin: 2rem auto 1rem auto; text-align: center;">
  <img src="../images/banner-aas-mcp-purple-h167.png" alt="Shellsmith logo">
</div>

# MCP Integration

**aas-mcp** provides a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that enables AI assistants to interact with Asset Administration Shells through the Shellsmith ecosystem.

---

## What is MCP?

The Model Context Protocol (MCP) is an open standard for connecting AI assistants to external data sources and tools. It allows AI models to securely access and interact with various services, databases, and APIs through a standardized interface.

MCP servers expose capabilities as **tools** that AI assistants can invoke to perform specific tasks, like querying databases, calling APIs, or managing resources.

---

## Installation

**aas-mcp** is automatically installed when you install Shellsmith with the optional `mcp` dependency `shellsmith[mcp]`.
You can also install **aas-mcp** independently:

```bash
pip install aas-mcp
```

---

##  MCP Client Configuration

### Claude Desktop

Add **aas-mcp** to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "aas-mcp": {
      "command": "aas-mcp",
      "env": {
        "SHELLSMITH_BASYX_ENV_HOST": "http://localhost:8081"
      }
    }
  }
}
```

### Other MCP Clients

The configuration format is similar for other MCP-compatible clients like [LM Studio](https://lmstudio.ai/), [Continue](https://continue.dev/), or custom MCP implementations.

Consult your client's documentation for the specific configuration syntax.

---

## BaSyx Environment Configuration

The MCP server connects to an Eclipse BaSyx environment. Configure the connection using:

### Environment Variable

```bash
export SHELLSMITH_BASYX_ENV_HOST=https://your-basyx-host:8081
```

### `.env` File

Create a `.env` file in your working directory:

```dotenv
SHELLSMITH_BASYX_ENV_HOST=https://your-basyx-host:8081
```

### Dynamic Configuration

Each MCP tool accepts an optional `host` parameter to override the default configuration on a per-request basis.

---

## Available MCP Tools

The **aas-mcp** server exposes 25+ tools for comprehensive AAS management:

### Shell Management

| Tool           | Description                                        |
|----------------|----------------------------------------------------|
| `get_shells`   | Retrieve all available Asset Administration Shells |
| `get_shell`    | Get a specific Shell by its identifier             |
| `create_shell` | Create a new Asset Administration Shell            |
| `update_shell` | Update an existing Shell (full replacement)        |
| `delete_shell` | Delete a Shell and optionally its Submodels        |

### Submodel Management

| Tool                    | Description                                         |
|-------------------------|-----------------------------------------------------|
| `get_submodels`         | Retrieve all available Submodels                    |
| `get_submodel`          | Get a specific Submodel by its identifier           |
| `create_submodel`       | Create a new Submodel                               |
| `update_submodel`       | Update an existing Submodel (full replacement)      |
| `delete_submodel`       | Delete a Submodel and optionally unlink from Shells |
| `get_submodel_value`    | Get the raw `$value` of a Submodel                  |
| `update_submodel_value` | Update the `$value` of a Submodel (partial update)  |
| `get_submodel_metadata` | Get the `$metadata` of a Submodel                   |

### Submodel Element Management

| Tool                            | Description                                        |
|---------------------------------|----------------------------------------------------|
| `get_submodel_elements`         | Get all elements from a Submodel                   |
| `get_submodel_element`          | Get a specific element by its path                 |
| `create_submodel_element`       | Create a new Submodel Element                      |
| `update_submodel_element`       | Update an existing element (full replacement)      |
| `delete_submodel_element`       | Delete a Submodel Element                          |
| `get_submodel_element_value`    | Get the raw `$value` of a Submodel Element         |
| `update_submodel_element_value` | Update the `$value` of an element (partial update) |

### Reference Management

| Tool                  | Description                              |
|-----------------------|------------------------------------------|
| `get_submodel_refs`   | Get all Submodel references from a Shell |
| `create_submodel_ref` | Create a Submodel reference in a Shell   |
| `delete_submodel_ref` | Remove a Submodel reference from a Shell |

### Health & Monitoring

| Tool                | Description                                      |
|---------------------|--------------------------------------------------|
| `get_health_status` | Check the health status of the BaSyx environment |
| `is_healthy`        | Boolean check for environment health             |

---

## Starting the Server

Run the MCP server directly:

```bash
aas-mcp
```

The server runs in **stdio mode** by default. It will listen for MCP requests and respond with tool results.

!!! note  
    The server typically runs as a background process managed by your MCP client (like Claude Desktop).
