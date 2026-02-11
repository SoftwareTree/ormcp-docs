Copyright (c) 2025, Software Tree

# ORMCP Server - Beta

*A Model Context Protocol (MCP) Server to connect your AI applications to relational databases*

ORMCP Server enables AI LLMs and MCP clients to easily exchange object-oriented data (in JSON format) with any relational database using the MCP standard protocol.

**ORMCP Server makes your relational data AI ready.**

## ⚠️ Beta Notice

**ORMCP Server** is currently in **Beta**, and we are offering early access to users who want to check the software, provide feedback, and help us ensure the product meets the highest quality standards. This Beta version is **not** intended for commercial use, and it is provided for **testing purposes only**.

## 📋 Table of Contents

* [What is MCP?](#what-is-mcp)
* [Features](#-features)
* [How It Works](#how-it-works)
* [Quick Start](#-quick-start)
* Platform-Specific Guides — 🍎 [macOS](./guides/getting-started-mac.md) · 🪟 [Windows](./guides/getting-started-windows.md) · 🐧 [Linux](./guides/getting-started-linux.md)
* [Installation](#ormcp-package-installation)
* [Gilhari Microservice Setup](#gilhari-microservice-setup)
* [Configuration](#configuration-for-ormcp-server)
* [Starting the Server](#starting-the-server)
* [Client Configuration](#mcp-client-configuration)
* [Usage Examples](#usage-examples)
* [MCP Tools Reference](#mcp-tools-reference)
* [Troubleshooting](#troubleshooting)
* [Development](#development)
* [Contributing](#contributing)
* [License](#license)
* [Support & Resources](#support--resources)

## What is MCP?

The Model Context Protocol (MCP) is an open standard that provides a unified way for AI models to interact with external tools and data sources. It standardizes communication, making it easier to integrate LLMs into complex workflows without building custom API integrations for every use case.

Learn more at the [Official MCP Website](https://modelcontextprotocol.io/).

## ✨ Features

* **✅ Standardized Interface:** Fully compliant with the Model Context Protocol (MCP) specification
* **🌐 Database Agnostic:** Works with any JDBC-compliant database (e.g., PostgreSQL, MySQL, Oracle, SQL Server, DB2, SQLite)
* **↔️ Bi-directional Data Flow:** Seamless AI ↔ Database communication with optional support for only READONLY operations
* **🔄 Object-Relational Mapping (ORM):** JSON object operations (CRUD) transparently mapped to relational data
* **🔒 Secure Data Access**: Domain model-specific operations promote data protection
* **🧾 Declarative ORM Specification:** Intuitive, non-intrusive, and flexible ORM specification based on a simple grammar
* **🕸️ Support for Complex Object Modeling:** Including one-to-one, one-to-many, and many-to-many relationships, and path-expressions
* **🖇️ Flexible Queries:** Deep and Shallow queries, Various operational directives similar to **GraphQL** capabilities to refine the shape and scope of returned objects
* **🚀 Highly Optimized and Lightweight Mapping Engine:** Connection pooling, Prepared statements, Optimized SQL statements, Minimal database trips, Caching of metadata
* **🔌 Compatible with Existing Data and Databases:** Works with existing schemas and data in any database; Does not require any native JSON data type
* **📚 Comprehensive Documentation:** Detailed User manual and README files, API documentation, sample apps
* **☁️ Cloud Agnostic:** Deploy anywhere with Docker support
* **⚡ High Performance:** Built on versatile Gilhari microservice architecture and optimised ORM engine
* **🛡️ Robust Error Handling:** Clear error messages and recovery mechanisms
* **📈 Scalable:** Handles multiple concurrent requests efficiently; Scalable Docker deployment

## How It Works

```
+---------------------+         +----------------------+         +-------------------------+
| AI App / LLM Client | <--->   |     ORMCP Server     | <--->   |   Relational Database   |
| (MCP-compliant tool)|         |    (MCP + Gilhari)   |         | (Postgres, MySQL, etc.) |
+---------------------+         +----------------------+         +-------------------------+
         |                                |                                 |
         |  JSON (via MCP Tools)          |                                 |
         |------------------------------->|                                 |
         |                                |   ORM + JDBC                    |
         |                                |-------------------------------->|
         |                                |                                 |
         |     JSON result (MCP format)   |                                 |
         |<-------------------------------|                                 |
```

**Important:** The AI application (LLM client) translates natural language into MCP tool calls. ORMCP Server then translates these MCP tool calls into REST API calls to Gilhari.

**ORMCP Server** bridges the gap between modern AI applications and relational databases through:

* **MCP Protocol**: Standardized AI-to-tool communication
* **Gilhari**: Integration layer with relational databases via ORM and JDBC
* **JSON Mapping**: Transparent object-relational mapping

## 🚀 Quick Start

> **New to ORMCP? Jump straight to your platform-specific guide for a streamlined setup:**
> 🍎 [macOS](./guides/getting-started-mac.md) · 🪟 [Windows](./guides/getting-started-windows.md) · 🐧 [Linux](./guides/getting-started-linux.md)
>
> The sections below cover all platforms together as a complete reference.

### Three Simple Steps to Use ORMCP

**1. Scope Your Data**

* Define lightweight object models for your relevant data
* Write a declarative ORM specification for those models in a text file using a simple (JDX) grammar

**2. Build Your Gilhari Microservice**

* Add models, ORM specification, and JDBC driver to a Dockerfile
* Build the Gilhari Docker image

**3. Run with ORMCP**

* Connect ORMCP to the Gilhari microservice
* Start Gilhari, then ORMCP
* Interact with scoped relational data in an intuitive, object-oriented way using an AI Agent or MCP client

---

### Detailed Quick Start

#### Prerequisites

* Python 3.12+
* Docker (for Gilhari microservice)
* JDBC driver for your target database

#### 1. Install ORMCP Server

> **Platform-specific guides** with step-by-step install instructions for your OS:
> [macOS](./guides/getting-started-mac.md) · [Windows](./guides/getting-started-windows.md) · [Linux](./guides/getting-started-linux.md)

**For Beta Users (Gemfury Private PyPI):**

Request beta access and receive your token at: [softwaretree.com/products/ormcp](https://www.softwaretree.com)

```
# Install with token
# Note: --extra-index-url is required because build dependencies (like hatchling) 
# are available on PyPI but not on Gemfury
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server

# Verify installation
pip show ormcp-server
```

Replace `YOUR_TOKEN` with your beta access token.

> **📌 Linux/Mac Users:** Modern Linux distributions and macOS may require virtual environments. See your [platform guide](#-quick-start) or the [troubleshooting guide](https://github.com/softwaretree/ormcp-docs/blob/main/guides/troubleshooting.md#externally-managed-environment-error) if you get "externally-managed-environment" errors.

```
# Create virtual environment (recommended on Linux/Mac)
python3 -m venv .venv

# Activate — Linux/Mac:
source .venv/bin/activate
# Activate — Windows (Command Prompt):
.venv\Scripts\activate
# Activate — Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install with token
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server
```

**For Production Users (PyPI):**

```
# Install from PyPI (available after beta)
pip install ormcp-server

# Verify installation
pip show ormcp-server
```

**If `ormcp-server` command is not found after installation:**

Add the Python executable directory to your PATH. See your platform guide for details:
[macOS](./guides/getting-started-mac.md#troubleshooting) · [Windows](./guides/getting-started-windows.md#troubleshooting) · [Linux](./guides/getting-started-linux.md#troubleshooting)

#### 2. Set Up Gilhari Microservice

See detailed setup in [Gilhari Microservice Setup](#gilhari-microservice-setup) section below.

**Note:** A complete working example is available in a separate repository: **[gilhari\_example1](https://github.com/SoftwareTree/gilhari_example1)**

To run the example:

**IMPORTANT:** Docker is required for building and running a Gilhari microservice — **[Get Docker](https://docs.docker.com/get-docker/)** if not already installed on your machine

```
# Clone the example repository of a sample Gilhari microservice that deals with User type of objects
git clone https://github.com/SoftwareTree/gilhari_example1.git
cd gilhari_example1

# Pull Gilhari Docker image
docker pull softwaretree/gilhari:latest

# Build a Docker image for the sample Gilhari microservice
./build.cmd  # On Windows
# or
./build.sh   # On Linux/Mac

# Run the sample microservice
docker run -p 80:8081 gilhari_example1:1.0

# Optionally, populate the database with sample data
./curlCommandsPopulate.cmd  # On Windows
# or
./curlCommandsPopulate.sh   # On Linux/Mac
```

#### 3. Configure Environment

```
# Linux/Mac
export GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
export MCP_SERVER_NAME="MyORMCPServer"

# Windows (Command Prompt)
set GILHARI_BASE_URL=http://localhost:80/gilhari/v1/
set MCP_SERVER_NAME=MyORMCPServer

# Windows (PowerShell)
$env:GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
$env:MCP_SERVER_NAME="MyORMCPServer"
```

#### 4. Start the ORMCP Server

```
ormcp-server
```

**If you get command not found errors, see your platform guide:**
[macOS](./guides/getting-started-mac.md#troubleshooting) · [Windows](./guides/getting-started-windows.md#troubleshooting) · [Linux](./guides/getting-started-linux.md#troubleshooting)

```
# Or use Python directly (works on all platforms)
python -m ormcp_server
```

#### 5. Connect Your AI Client

For **Claude Desktop**, add to `claude_desktop_config.json`:

**Option 1: Using command name (requires PATH configured):**

```
{
  "mcpServers": {
    "my-ormcp-server": {
      "command": "ormcp-server",
      "args": [],
      "env": {
        "GILHARI_BASE_URL": "http://localhost:80/gilhari/v1/",
        "MCP_SERVER_NAME": "MyORMCPServer"
      }
    }
  }
}
```

**Option 2: Using full path (recommended for Windows):**

```
{
  "mcpServers": {
    "my-ormcp-server": {
      "command": "C:\\Users\\<YourUsername>\\AppData\\Roaming\\Python\\Python313\\Scripts\\ormcp-server.exe",
      "args": [],
      "env": {
        "GILHARI_BASE_URL": "http://localhost:80/gilhari/v1/",
        "MCP_SERVER_NAME": "MyORMCPServer"
      }
    }
  }
}
```

**To find your exact path:**

```
# Windows (PowerShell)
(Get-Command ormcp-server).Source

# Or use pip
pip show -f ormcp-server | findstr "Location"

# Linux/Mac
which ormcp-server
```

You're ready! Your AI client can now interact with your database using natural language.

**Note:** Steps 3 (Configure Environment) and 4 (Start the ORMCP Server) are not necessary if you are using Claude Desktop as a client because Claude Desktop automatically starts a configured ORMCP server in STDIO mode.

## Usage Examples

### Query Data

**AI Prompt:** *"Show me all users with age greater than or equal to 55"*

**Generated MCP Call:**

```
{
  "name": "query",
  "arguments": {
    "className": "User",
    "filter": "age >= 55",
    "maxObjects": -1,
    "deep": true
  }
}
```

**Result:**

```
[
  {"id": 55, "name": "Mary55", "city": "Campbell", "state": "CA"},
  {"id": 56, "name": "Mike56", "city": "Boston", "state": "MA"}
]
```

### Insert Data

**AI Prompt:** *"Add a new User (id = 65) named John Smith of Boston, MA with age of 65"*

**Generated MCP Call:**

```
{
  "name": "insert",
  "arguments": {
    "className": "User",
    "jsonObjects": [
      {
        "id": 65,
        "name": "John Smith",
        "city": "Boston",
        "state": "MA",
        "age": 65
      }
    ]
  }
}
```

### Aggregate Data

**AI Prompt:** *"What's the average age of users in California?"*

**Generated MCP Call:**

```
{
  "name": "getAggregate",
  "arguments": {
    "className": "User",
    "attributeName": "age",
    "aggregateType": "AVG",
    "filter": "state='CA'"
  }
}
```

**Result:**

```
49
```

## Gilhari Microservice Setup

**ORMCP Server** depends on **Gilhari software**, a microservice framework for JSON data integration with databases. This setup must be completed before starting the ORMCP server.

**IMPORTANT:** Docker is required for building and running a Gilhari microservice — **[Get Docker](https://docs.docker.com/get-docker/)** if not already installed on your machine

### Install Gilhari Software

1. **Pull the Gilhari Docker image:**

   ```
   docker pull softwaretree/gilhari:latest
   ```
2. **Install the Gilhari SDK:**

   * The **SDK** for **Gilhari software** is bundled in the **ORMCP Server** package under the **Gilhari\_SDK** folder
   * Alternatively, download from: <https://www.softwaretree.com/v1/products/gilhari/download-gilhari.php>
   * The **SDK** includes documentation (READMEs, API guides, sample applications) to help you use **Gilhari software** easily

### Configure Your App-Specific Gilhari Microservice

Follow these steps (detailed in Gilhari SDK documentation):

1. **Define domain model classes** - Java container classes for your JSON objects
2. **Create declarative ORM specification** - Map JSON attributes to database schema
3. **Build Docker image of the app-specific Gilhari microservice** - Include domain classes, ORM specification, and JDBC driver
4. **Run the microservice:**

   ```
   docker run -p 80:8081 your-gilhari-service:1.0
   ```

**Note:** A complete working example is available in a separate repository: **[gilhari\_example1](https://github.com/SoftwareTree/gilhari_example1)**. This example demonstrates a Gilhari microservice that manages **User** objects.

### Quick Start with Example:

```
# Clone the example repository
git clone https://github.com/SoftwareTree/gilhari_example1.git
cd gilhari_example1

# Build a Docker image for the sample Gilhari microservice
./build.cmd  # On Windows
# or
./build.sh   # On Linux/Mac

# Run the sample microservice
docker run -p 80:8081 gilhari_example1:1.0

# Optionally, populate the database with sample data
./curlCommandsPopulate.cmd  # On Windows
# or
./curlCommandsPopulate.sh   # On Linux/Mac
```

For detailed setup and configuration instructions, see the [gilhari\_example1 README](https://github.com/SoftwareTree/gilhari_example1/blob/main/README.md).

## ORMCP Package Installation

### Recommended: Virtual Environment

```
# Create and activate virtual environment
python -m venv .venv

# Activate the environment
# Linux/Mac:
source .venv/bin/activate
# Windows (Command Prompt):
.venv\Scripts\activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install ORMCP Server
# Beta (Gemfury):
# Note: --extra-index-url is required because build dependencies (like hatchling) 
# are available on PyPI but not on Gemfury
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server

# Production (PyPI) - available after beta:
# pip install ormcp-server
```

Replace `YOUR_TOKEN` with your beta access token from [softwaretree.com/products/ormcp](https://www.softwaretree.com).

### Global Installation

**Beta (Gemfury):**

```
# Note: --extra-index-url is required because build dependencies (like hatchling) 
# are available on PyPI but not on Gemfury
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server
```

Replace `YOUR_TOKEN` with your beta access token.

**Production (PyPI) - available after beta:**

```
pip install ormcp-server
```

**Note:** When installing globally (without a virtual environment), the `ormcp-server` executable will be installed to your user's Python Scripts directory. See your [platform guide](#-quick-start) if you encounter "command not found" errors.

### Accessing Full Package with SDK and Examples

To access the complete package including Gilhari SDK, examples, and documentation:

**Beta (Gemfury):**

```
# Download source distribution
# Note: --extra-index-url is required because build dependencies (like hatchling) 
# are available on PyPI but not on Gemfury
pip download --no-binary :all: \
  --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server

# Extract it (use the appropriate version number)
tar -xzf ormcp_server-*.tar.gz
cd ormcp_server-*/

# Now you have access to:
# - Gilhari_SDK/          (Complete SDK with documentation)
# - gilhari_example1/     (Ready-to-use example microservice)
# - package/client/       (Example client code)
# - package/docs/         (Additional documentation)
```

Replace `YOUR_TOKEN` with your beta access token.

**Production (PyPI) - available after beta:**

```
# Download source distribution
pip download --no-binary :all: ormcp-server

# Extract it
tar -xzf ormcp_server-*.tar.gz
cd ormcp_server-*/
```

**Windows users:** If you don't have `tar` installed, you can:

* Use 7-Zip or WinRAR to extract the .tar.gz file
* Or use PowerShell: `tar -xzf ormcp_server-*.tar.gz`
* Or download directly from the Gemfury/PyPI website

## Package Contents

The ORMCP Server package includes additional resources beyond the Python code:

### Runtime Installation (Wheel)

When you install via pip, you get the core Python package needed to run ORMCP Server:

```
pip install ormcp-server
```

This installs only the essential runtime files to your Python environment.

### Full Package with SDK and Documentation (Source Distribution)

The complete package includes:

* **Gilhari\_SDK/** - Complete SDK with documentation, examples, and tools for creating custom Gilhari microservices
* **gilhari\_example1/** - Ready-to-use example Gilhari microservice
* **package/client/** - Example client code and usage documentation
* **package/docs/** - Additional technical documentation
* **pyproject.toml** - Build configuration
* **README.md** - This file
* **LICENSE** - License terms

### Accessing the Full Package

**Option 1: Download from PyPI/Gemfury**

**Beta (Gemfury):**

```
# Download the source distribution (.tar.gz)
# Note: --extra-index-url is required because build dependencies (like hatchling) 
# are available on PyPI but not on Gemfury
pip download --no-binary :all: \
  --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server

# Extract it (use the appropriate version number; e.g., 0.5.x)
tar -xzf ormcp_server-0.5.x.tar.gz
cd ormcp_server-0.5.x

# Now you have access to:
# - Gilhari_SDK/
# - gilhari_example1/
# - package/client/
# - package/docs/
```

Replace `YOUR_TOKEN` with your beta access token.

**Production (PyPI) - available after beta:**

```
# Download the source distribution
pip download --no-binary :all: ormcp-server

# Extract it
tar -xzf ormcp_server-*.tar.gz
cd ormcp_server-*/
```

**Windows users:** If you don't have `tar` installed, you can:

* Use 7-Zip or WinRAR to extract the .tar.gz file
* Or use PowerShell: `tar -xzf ormcp_server-0.5.x.tar.gz`
* Or download directly from the Gemfury/PyPI website

**Option 2: Download from Package Page**

**Beta:** Contact [ormcp\_support@softwaretree.com](mailto:ormcp_support@softwaretree.com) for direct download links.

**Production (after beta):** Visit <https://pypi.org/project/ormcp-server/> and download the `.tar.gz` file.

Look for the "Download files" section and download the source distribution (`.tar.gz`).

### Using the Gilhari SDK

After extracting the source distribution:

```
# Navigate to the SDK
cd Gilhari_SDK

# Read the documentation
# - Check README files for setup instructions
# - Review examples in the examples/ directory
# - See API documentation for ORM specification details

# The SDK includes:
# - Gilhari Docker base image information
# - Documentation (READMEs, API guides)
# - Sample applications
# - Tools for reverse-engineering ORM from existing databases
# - JDX grammar specification
```

### Running the Example Gilhari Microservice

```
# Navigate to the example
cd gilhari_example1

# Follow the README.md in that directory to:
# 1. Build the Docker image
# 2. Run the microservice
# 3. Populate sample data
# 4. Test with ORMCP Server
```

**Why Two Package Formats?**

* **Wheel (.whl)** - Binary distribution, fast to install, includes only runtime code (~50KB)
* **Source Distribution (.tar.gz)** - Complete package with all resources (~several MB)

Most users only need the wheel for running ORMCP Server. Download the source distribution if you need:

* The Gilhari SDK for creating custom microservices
* Example applications and client code
* Complete documentation
* Additional technical guides

## Configuration for ORMCP Server

Configure via environment variables:

| Variable | Description | Default | Example |
| --- | --- | --- | --- |
| `GILHARI_BASE_URL` | Gilhari microservice URL | `http://localhost:80/gilhari/v1/` | `http://myhost:8888/gilhari/v1/` |
| `MCP_SERVER_NAME` | Server identifier | `ORMCPServerDemo` | `MyCompanyORMCP` |
| `GILHARI_TIMEOUT` | API timeout (seconds) | `30` | `60` |
| `LOG_LEVEL` | Logging verbosity | `INFO` | `DEBUG`, `WARNING`, `ERROR` |
| `READONLY_MODE` | Expose only read operations | `False` | `True` |
| `GILHARI_NAME` | Name of the app-specific Gilhari microservice | "" | `my-gilhari-microservice` |
| `GILHARI_IMAGE` | Docker image name of the app-specific Gilhari microservice | "" | `gilhari_example1:1.0` |
| `GILHARI_HOST` | IP address of the host machine for Gilhari microservice | `localhost` | `10.20.30.40` |
| `GILHARI_PORT` | Port number to contact the Gilhari microservice | `80` | `8888` |

**Notes:**

* If `READONLY_MODE` is set to `True`, the MCP tools that can potentially modify the data (e.g., insert, update, update2, delete, delete2) are not exposed by the **ORMCP server** to the MCP client. By default, all MCP tools are exposed.
* `GILHARI_BASE_URL` and `GILHARI_NAME` are used to probe an already running Gilhari microservice container
* `GILHARI_IMAGE`, `GILHARI_NAME`, and `GILHARI_PORT` are used to run a new instance of Gilhari microservice if an existing microservice is not found. Please make sure that the values of `GILHARI_HOST` and `GILHARI_PORT` variables match the corresponding values in `GILHARI_BASE_URL` setting because that is where the **ORMCP server** will contact the Gilhari microservice.

### Configuration Example

```
# Linux/Mac
export GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
export GILHARI_TIMEOUT="30"
export MCP_SERVER_NAME="MyORMCPServer"
export LOG_LEVEL="INFO"

# Windows (Command Prompt)
set GILHARI_BASE_URL=http://localhost:80/gilhari/v1/
set GILHARI_TIMEOUT=30
set MCP_SERVER_NAME=MyORMCPServer
set LOG_LEVEL=INFO

# Windows (PowerShell)
$env:GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
$env:GILHARI_TIMEOUT="30"
$env:MCP_SERVER_NAME="MyORMCPServer"
$env:LOG_LEVEL="INFO"
```

## Starting the Server

### Standard Mode (Recommended)

Activate your virtual environment (if using one):

```
# Linux/Mac
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Start the server using the CLI command:

```
ormcp-server
```

This runs the MCP server in stdio mode via the `main.py` entry point.

**Troubleshooting — Command Not Found:**

If you get `'ormcp-server' is not recognized` or `command not found`, see your platform guide for PATH configuration and fix options:
[macOS](./guides/getting-started-mac.md#troubleshooting) · [Windows](./guides/getting-started-windows.md#troubleshooting) · [Linux](./guides/getting-started-linux.md#troubleshooting)

```
# Use Python directly on any platform (always works)
python -m ormcp_server
```

### Using Source Code Directly (Advanced)

**Note:** Requires source distribution. Download with:

```
# Note: --extra-index-url is required because build dependencies (like hatchling) 
# are available on PyPI but not on Gemfury
pip download --no-binary :all: \
  --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server
tar -xzf ormcp_server-*.tar.gz
cd ormcp_server-*/
```

Run the server directly with Python:

```
python src/ormcp_server.py
```

This bypasses the CLI wrapper and runs the server directly.

### Alternative Methods (Advanced Users)

**Direct executable execution:**

```
# Windows
.venv\Scripts\ormcp-server.exe

# Linux/Mac
.venv/bin/ormcp-server
```

**Using fastmcp CLI (requires source distribution):**

```
fastmcp run src/ormcp_server.py
```

**Using MCP Inspector dev mode (requires source distribution):**

```
mcp dev src/ormcp_server.py
```

**Using MCP Inspector without source code:**

If you have the `ormcp-server` package installed, you can use MCP Inspector to explore the server's capabilities:

```
# Using the installed package
npx @modelcontextprotocol/inspector python -m ormcp_server

# Or if you have the command in PATH
npx @modelcontextprotocol/inspector ormcp-server
```

This allows you to interactively test and explore ORMCP Server tools without needing the source distribution.

### HTTP or SSE Transport Support

> **Note:** Currently only the `stdio` transport is fully supported out of the box. Support for HTTP or SSE transports is experimental.

You can start the ORMCP server in HTTP mode from the command line:

```
# Basic HTTP mode
python src/ormcp_server.py --transport http

# Or using the CLI
ormcp-server --mode http
```

**Customize host and port:**

```
python src/ormcp_server.py --transport http --host 0.0.0.0 --port 9000

# Or using CLI
ormcp-server --mode http --host 0.0.0.0 --port 9000
```

**Available command-line options:**

* `--mode` / `--transport`: Choose between "stdio" (default) or "http"
* `--host`: Set the host address (default: 127.0.0.1, only used in HTTP mode)
* `--port`: Set the port number (default: 8080, only used in HTTP mode)

**Quick HTTP setup:**

```
python src/ormcp_server.py --transport http
# or
ormcp-server --mode http
```

Make sure you have `uvicorn` installed as a dependency since HTTP mode uses it to serve the application.

#### Usage in HTTP Mode

The MCP server running in HTTP mode isn't designed to be accessed directly through a web browser. It's an API server that expects specific MCP protocol messages, not HTTP GET requests to the root path.

### Summary

* Use `ormcp-server` CLI for the cleanest, recommended experience.
* Use direct `python src/ormcp_server.py` for simple runs with source distribution.
* Use `mcp dev` or `fastmcp run` for advanced dev/testing scenarios with source distribution.

### Expected Output

```
[INFO] ORMCP server name: ORMCPServerDemo
[INFO] GILHARI BASE URL: http://localhost:80/gilhari/v1/
[INFO] ORMCP server v0.5.x starting in stdio (or http) mode ...
```

## MCP Client Configuration

### Claude Desktop

> **Platform-specific config file locations and path setup:**
> [macOS](./guides/getting-started-mac.md#step-5-connect-your-ai-client) · [Windows](./guides/getting-started-windows.md#step-5-connect-your-ai-client) · [Linux](./guides/getting-started-linux.md#step-5-connect-your-ai-client)

#### Option 1: Using Command Name (Requires PATH Configured)

```
{
  "mcpServers": {
    "my-ormcp-server": {
      "command": "ormcp-server",
      "args": [],
      "env": {
        "GILHARI_BASE_URL": "http://localhost:80/gilhari/v1/",
        "MCP_SERVER_NAME": "MyORMCPServer"
      }
    }
  }
}
```

#### Option 2: Using Full Path (Recommended for Windows)

```
{
  "mcpServers": {
    "my-ormcp-server": {
      "command": "C:\\Users\\<YourUsername>\\AppData\\Roaming\\Python\\Python313\\Scripts\\ormcp-server.exe",
      "args": [],
      "env": {
        "GILHARI_BASE_URL": "http://localhost:80/gilhari/v1/",
        "MCP_SERVER_NAME": "MyORMCPServer"
      }
    }
  }
}
```

**To find your exact installation path:**

```
# Windows (PowerShell)
(Get-Command ormcp-server).Source

# Windows (Command Prompt)
where ormcp-server

# Linux/Mac
which ormcp-server

# Any platform
pip show -f ormcp-server | grep "ormcp-server.exe"  # Windows
pip show -f ormcp-server | grep "ormcp-server$"     # Linux/Mac
```

#### Option 3: Direct Python Execution

```
{
  "mcpServers": {
    "my-ormcp-server": {
      "command": "python", 
      "args": [
        "-m",
        "ormcp_server"
      ],
      "env": {
        "GILHARI_BASE_URL": "http://localhost:80/gilhari/v1/",
        "MCP_SERVER_NAME": "MyORMCPServer"
      }
    }
  }
}
```

#### Option 4: Using FastMCP (For Developers with Source Distribution)

```
{
  "mcpServers": {
    "ORMCPServerDemo": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "<path_to_your_ormcp-server-project>/src/ormcp_server.py"
      ],
      "env": {
        "GILHARI_BASE_URL": "http://localhost:80/gilhari/v1/",
        "MCP_SERVER_NAME": "MyORMCPServer"
      }
    }
  }
}
```

#### Option 5: HTTP Mode (Experimental)

```
{
  "mcpServers": {
    "my-ormcp-server-http": {
      "command": "ormcp-server",
      "args": [
        "--mode", "http",
        "--port", "8080"
      ],
      "env": {
        "GILHARI_BASE_URL": "http://localhost:80/gilhari/v1/",
        "MCP_SERVER_NAME": "MyORMCPServer"
      }
    }
  }
}
```

**Notes:**

* `ORMCPServerDemo` is the default name of the ORMCP server.
* Replace `<YourUsername>` with your actual Windows username
* If you are providing a port number of the associated Gilhari microservice through the "GILHARI\_BASE\_URL" environment variable, make sure that is the port where that Gilhari microservice is listening.
* *Note: As of July 20, 2025, Claude desktop did not support connecting to an MCP server running in http mode.*

### Gemini CLI

Update the Gemini `settings.json` file:

```
{
  "mcpServers": {
    "my-ormcp-server-http": {
      "httpUrl": "http://127.0.0.1:8080/mcp"
    }
  }
}
```

*Note: Gemini CLI currently requires HTTP mode.*

### OpenAI GPTs (Developer Mode)

To connect the ORMCP server to a custom GPT in developer mode, the server must be running in HTTP mode and be accessible from a public URL.

1. **Prepare the Backend:**

   * First, ensure the **Gilhari microservice** is compiled and running in its Docker container as per the setup instructions.
   * Use `curl` to verify the Gilhari service is responsive:

     ```
     curl -i http://localhost:80/gilhari/v1/getObjectModelSummary/now
     ```
2. **Configure and Run the ORMCP Server:**

   * Set the required environment variables for the ORMCP server to connect to Gilhari.

     ```
     export GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
     export MCP_SERVER_NAME="MyORMCPServer"
     export GILHARI_TIMEOUT="30"
     export LOG_LEVEL="INFO"
     ```
   * Start the ORMCP server in **HTTP mode**, as this is required for web-based clients.

     ```
     # Run from the project's root directory
     ormcp-server --mode http --port 8080
     ```
3. **Expose the Server with a Public URL:**
   OpenAI's servers need a public web address to reach your local ORMCP server. Use a tunneling service like `cloudflared` or `ngrok` to create a secure public URL that forwards to your local machine.

   * **Option A: Using `cloudflared` (Recommended)**

     + In a new terminal, start a Cloudflare tunnel pointing to your server's port.

       ```
       cloudflared tunnel --url http://localhost:8080
       ```
     + `cloudflared` will provide a persistent public URL (e.g., `https://<your-tunnel-name>.trycloudflare.com`).
   * **Option B: Using `ngrok`**

     + In a new terminal, start `ngrok` to forward traffic to port 8080.

       ```
       ngrok http 8080
       ```
     + `ngrok` will provide a temporary public HTTPS URL (e.g., `https://random-string.ngrok-free.app`). Note that this URL changes every time you restart `ngrok` on the free plan.
4. **Connect to Your Custom GPT:**

   * Take the public URL generated by `cloudflared` or `ngrok`.
   * Append `/mcp` to the end of this URL. The final result will be your MCP endpoint, for example: `https://<your-public-url>/mcp`.
   * In your GPT's configuration settings (**Settings** → **Apps & Connectors** → **Create**), paste this complete URL into the MCP Server URL field. GPT will then discover and connect to the tools provided by your ORMCP server.

### Other MCP Clients

* Connect to ORMCP server and use the MCP compatible ORM tools provided by the ORMCP server.
* Configure according to your client's MCP server setup requirements using the appropriate transport mode (STDIO or HTTP).
* **📚 Integration Guides:** See detailed documentation on connecting to ORMCP Server:
  + [MCP Protocol Reference](https://github.com/softwaretree/ormcp-docs/blob/main/docs/mcp_protocol_reference.md) - Low-level JSON-RPC protocol details
  + [Using the ORMCP Client Example](https://github.com/softwaretree/ormcp-docs/blob/main/client/using_ormcp_client_example.md) - Python client usage guide
  + [Interacting with ORMCP Server in STDIO Mode](https://github.com/softwaretree/ormcp-docs/blob/main/docs/Interacting_With_ORMCP_Server_In_STDIO_Mode.md) - STDIO transport guide
  + [Interacting with ORMCP Server in HTTP Mode](https://github.com/softwaretree/ormcp-docs/blob/main/docs/Interacting_With_ORMCP_Server_In_HTTP_Mode.md) - HTTP transport guide
  + Additional guides available in the [documentation repository](https://github.com/softwaretree/ormcp-docs) (also included in the source distribution)

## MCP Tools Reference

ORMCP Server provides the following MCP tools for interacting with your database.

**📖 Detailed API Documentation:** For complete parameter specifications and technical details, see the [MCP Tools API Reference](https://github.com/softwaretree/ormcp-docs/blob/main/reference/ormcp_tools_reference.md).

**💡 Working Examples:** See real-world usage examples in the [examples directory](/SoftwareTree/ormcp-docs/blob/main/examples).

### Core Operations

#### `getObjectModelSummary`

Retrieve information about the underlying object model.

**Returns:** Information about classes (types), attributes, primary keys, and relationships in your domain model.

#### `query`

Query objects with filtering and relationship traversal.

**Parameters:**

* `className` (string): Type of objects to query
* `filter` (string, optional): SQL-like WHERE clause for filtering
* `maxObjects` (integer, optional): Maximum number of objects to retrieve (-1 for all, default: -1)
* `deep` (boolean, optional): Include referenced objects in results (default: true)
* `operationDetails` (string, optional): JSON array of operational directives for fine-tuning queries. Supports GraphQL-like operations such as:
  + `projections`: Retrieve only specific attributes
  + `ignore` or `follow`: Control referenced object branches
  + `filter`: Apply filters to referenced objects

#### `getObjectById`

Retrieve a specific object by its primary key.

**Parameters:**

* `className` (string): Type of object to retrieve
* `primaryKey` (object): Primary key values (single value or composite key object)
* `deep` (boolean, optional): Include referenced objects (default: true)
* `operationDetails` (string, optional): Operational directives for fine-tuning queries

#### `access`

Retrieve object(s) referenced by a specific attribute of a referencing object.

**Parameters:**

* `className` (string): Type of the referencing object
* `jsonObject` (object): The referencing object containing the reference
* `attributeName` (string): Name of the attribute whose referenced value(s) to retrieve
* `deep` (boolean, optional): Include referenced objects of retrieved objects as well (default: true)
* `operationDetails` (string, optional): Operational directives for fine-tuning queries

#### `getAggregate`

Calculate aggregate values across objects (COUNT, SUM, AVG, MIN, MAX).

**Parameters:**

* `className` (string): Type of objects to aggregate
* `attributeName` (string): Attribute to perform aggregation on
* `aggregateType` (string): Type of aggregation - `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
* `filter` (string, optional): SQL-like WHERE clause to filter objects before aggregation

### Data Modification Operations

#### `insert`

Save one or more JSON objects to the database.

**Parameters:**

* `className` (string): Type of objects to insert
* `jsonObjects` (array): List of JSON objects to save to the database
* `deep` (boolean, optional): Save referenced objects as well (default: true)

#### `update`

Update one or more existing objects with new values.

**Parameters:**

* `className` (string): Type of objects to update
* `jsonObjects` (array): List of objects with updated values (must include primary keys)
* `deep` (boolean, optional): Update referenced objects as well (default: true)

#### `update2`

Bulk update objects matching filter criteria.

**Parameters:**

* `className` (string): Type of objects to update
* `filter` (string): SQL-like WHERE clause to identify objects to update
* `newValues` (array): List of attribute names and their new values
* `deep` (boolean, optional): Update referenced objects as well (default: true)

#### `delete`

Delete specific objects from the database.

**Parameters:**

* `className` (string): Type of objects to delete
* `jsonObjects` (array): Objects to delete (primary keys required for identification)
* `deep` (boolean, optional): Delete referenced objects as well (default: true)

#### `delete2`

Bulk delete objects matching filter criteria.

**Parameters:**

* `className` (string): Type of objects to delete
* `filter` (string, optional): SQL-like WHERE clause to identify objects to delete (empty string deletes all objects of the specified class)
* `deep` (boolean, optional): Delete referenced objects as well (default: true)

**Note:** In `READONLY_MODE=True`, the MCP tools for data modification operations (`insert`, `update`, `update2`, `delete`, `delete2`) are not exposed to MCP clients.

## Troubleshooting

For common issues and solutions, see the [Complete Troubleshooting Guide](https://github.com/softwaretree/ormcp-docs/blob/main/guides/troubleshooting.md).

### Quick Troubleshooting

**Installation Issues:**

* Command not found → See your [platform guide](#-quick-start) for PATH configuration: [macOS](./guides/getting-started-mac.md#troubleshooting) · [Windows](./guides/getting-started-windows.md#troubleshooting) · [Linux](./guides/getting-started-linux.md#troubleshooting)
* Externally managed environment → Use virtual environment (see [troubleshooting guide](https://github.com/softwaretree/ormcp-docs/blob/main/guides/troubleshooting.md#externally-managed-environment-error))
* Empty executable → Reinstall package
* Missing dependencies → `pip install --force-reinstall ormcp-server`

**Gilhari Example Issues:**

* Shell script permission denied → `chmod +x *.sh` or use `sh build.sh` (Linux/Mac)
* Database connection errors → Verify JDBC driver in Gilhari

**Runtime Issues:**

* Server won't start → Check Gilhari is running
* Database connection errors → Verify JDBC driver in Gilhari
* MCP client connection issues → Check config file syntax

**Enable Debug Mode:**

```
# Linux/Mac
export LOG_LEVEL=DEBUG
ormcp-server

# Windows (Command Prompt)
set LOG_LEVEL=DEBUG
ormcp-server

# Windows (PowerShell)
$env:LOG_LEVEL="DEBUG"
ormcp-server
```

**Get Help:**

* Documentation: [github.com/softwaretree/ormcp-docs](https://github.com/softwaretree/ormcp-docs)
* Issues: [github.com/softwaretree/ormcp-docs/issues](https://github.com/softwaretree/ormcp-docs/issues)
* Email: [ormcp\_support@softwaretree.com](mailto:ormcp_support@softwaretree.com)

## Development

### Testing

For testing and development with the source distribution:

**Beta (Gemfury):**

```
# Download source distribution
# Note: --extra-index-url is required because build dependencies (like hatchling) 
# are available on PyPI but not on Gemfury
pip download --no-binary :all: \
  --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server
tar -xzf ormcp_server-*.tar.gz
cd ormcp_server-*/

# Install in development mode
pip install -e ".[dev]"

# Run tests (if available in source distribution)
pytest
```

Replace `YOUR_TOKEN` with your beta access token.

**Production (PyPI) - available after beta:**

```
# Download source distribution
pip download --no-binary :all: ormcp-server
tar -xzf ormcp_server-*.tar.gz
cd ormcp_server-*/

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

### Gilhari Microservice Development

* **ORMCP Server** leverages **Gilhari software**, a RESTful microservice framework for JSON data integration with databases.
* You first create a custom Gilhari microservice based on the object relational data models of your application.
* An object relational mapping (ORM) specification defines and controls the scope and shape of your object model corresponding to your relational model.
* The ORM specification is defined declaratively in a text file (.jdx) based on a simple grammar.
* You may be able to reverse-engineer ORM specification from an existing database schema using tools/examples provided with Gilhari SDK. Check the `examples\JDX_ReverseEngineeringJSONExample` directory.
* The reverse-engineering example is also available online at [github.com/SoftwareTree/JDX\_ReverseEngineeringJSONExample](https://github.com/SoftwareTree/JDX_ReverseEngineeringJSONExample)
* For details on creating custom Gilhari microservices, refer to the Gilhari SDK documentation included in the source distribution package.
* Although an ORMCP server may start a Gilhari microservice if configured to do so (using `GILHARI_IMAGE`, `GILHARI_NAME`, and `GILHARI_PORT` environment variables), it is recommended that you start your custom Gilhari microservice before using the ORMCP server. Also, please make sure that the port number in the 'GILHARI\_BASE\_URL' environment variable for the ORMCP server matches the port number on which the custom Gilhari microservice is listening for incoming REST calls.

## Contributing

Thank you for your interest in ORMCP Server!

### 🚫 No Code Contributions at This Time

ORMCP Server is proprietary software. We are **not accepting** code contributions, pull requests, or feature submissions.

### 🐞 Feedback and Bug Reports

We **welcome feedback** on the beta version! You can help us improve ORMCP Server by:

* Reporting bugs or issues
* Suggesting improvements
* Sharing your experience

### How to Provide Feedback

* **GitHub Issues**: [Report issues or suggestions](https://github.com/softwaretree/ormcp-docs/issues)
* **Email**: [ormcp\_support@softwaretree.com](mailto:ormcp_support@softwaretree.com)

> Any feedback you provide may be used by Software Tree to improve the product, without any obligation to credit or compensate you.

## Third-Party Software

**Gilhari Dependency:**
ORMCP Server requires Gilhari microservice to function. Gilhari incorporates various third-party software components. For complete details of these third-party components and their licenses, see the LICENSE file in the Gilhari SDK or visit: <https://www.softwaretree.com/v1/products/gilhari/>

**Python Dependencies:**
ORMCP Server uses the following open-source Python libraries, each governed by their respective licenses:

* mcp (Model Context Protocol SDK)
* fastmcp (FastMCP framework)
* httpx (HTTP client library)
* pydantic (Data validation library)
* uvicorn (ASGI server)
* requests (HTTP library)

## License

ORMCP Server is proprietary software owned by Software Tree, LLC. See the [LICENSE](/SoftwareTree/ormcp-docs/blob/main/LICENSE) file for complete terms.

**Beta Evaluation:** ORMCP Server is currently available as a beta product under an evaluation license. This allows free use for testing and evaluation purposes for a limited evaluation period (approximately 2 months from first use).

**Gilhari Dependency:** ORMCP Server requires Gilhari microservice to function. By using ORMCP Server, you agree to comply with the Gilhari License Agreement as well. Gilhari incorporates various third-party software components. For details, see the LICENSE file in the Gilhari SDK or visit <https://www.softwaretree.com/v1/products/gilhari/>.

**Commercial Licensing:** Commercial licensing terms will be announced at the time of commercial release. For information or to express interest, contact Software Tree at [ormcp\_support@softwaretree.com](mailto:ormcp_support@softwaretree.com) or visit <https://www.softwaretree.com>.

## Support & Resources

* **Documentation**: [Complete documentation and guides](https://github.com/softwaretree/ormcp-docs)
* **Platform Guides**: [macOS](./guides/getting-started-mac.md) · [Windows](./guides/getting-started-windows.md) · [Linux](./guides/getting-started-linux.md)
* **Working Examples**: [Browse Examples](/SoftwareTree/ormcp-docs/blob/main/examples) | [Examples Guide](/SoftwareTree/ormcp-docs/blob/main/examples/README.md) - Real-world use cases and integrations
* **Example Microservice**: [gilhari\_example1 Repository](https://github.com/SoftwareTree/gilhari_example1)
* **Bug Reports**: [Report issues](https://github.com/softwaretree/ormcp-docs/issues)
* **Email Support**: [ormcp\_support@softwaretree.com](mailto:ormcp_support@softwaretree.com)
* **Gilhari Support**: [Software Tree Gilhari Documentation](https://www.softwaretree.com/v1/products/gilhari/gilhari_introduction.php)
* **MCP Protocol**: [Official MCP Site](https://modelcontextprotocol.io/)
* **Beta Access**: [Request token at softwaretree.com](https://www.softwaretree.com/products/ormcp)

---

**Made with ❤️ for the AI and database community**
