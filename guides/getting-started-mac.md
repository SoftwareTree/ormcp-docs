# Getting Started with ORMCP Server on macOS

> **Platform-specific guide** — This page consolidates all macOS instructions in one place.
> For the complete multi-platform reference, see the [main README](../README.md).

---

## Prerequisites

- **Python 3.12+** — Check your version: `python3 --version`
- **Docker** — Required for the Gilhari microservice. [Get Docker](https://docs.docker.com/get-docker/) if not already installed.
- **JDBC driver** for your target database (bundled in the Gilhari SDK)

---

## Step 1: Install ORMCP Server

### Recommended: Virtual Environment

Using a virtual environment is strongly recommended on modern macOS, which may refuse global pip installs with an "externally-managed-environment" error.

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install ORMCP Server (Beta — replace YOUR_TOKEN with your beta access token)
# Note: --extra-index-url is required because build dependencies (like hatchling)
# are available on PyPI but not on Gemfury
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server

# Verify installation
pip show ormcp-server
```

Request your beta access token at [softwaretree.com/products/ormcp](https://www.softwaretree.com/products/ormcp).

> **Production (after beta):** `pip install ormcp-server`

### Global Installation (Optional)

If you prefer a global install, the `ormcp-server` executable will be placed in `~/.local/bin/`. If the command is not found after installation, add it to your PATH (see [Troubleshooting](#troubleshooting) below).

```bash
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server
```

---

## Step 2: Set Up the Gilhari Microservice

ORMCP Server depends on **Gilhari**, a microservice that handles the ORM and database communication. You must have it running before starting ORMCP.

### Pull the Gilhari Docker Image

```bash
docker pull softwaretree/gilhari:latest
```

### Run the Example Microservice (Quickest Path)

A ready-to-use example microservice is available in a separate repository:

```bash
# Clone the example (manages User objects against a SQLite database)
git clone https://github.com/SoftwareTree/gilhari_example1.git
cd gilhari_example1

# Build the Docker image
./build.sh

# Run the microservice (listens on port 80)
docker run -p 80:8081 gilhari_example1:1.0

# (Optional) Populate the database with sample data
./curlCommandsPopulate.sh
```

### Build Your Own Gilhari Microservice

To connect ORMCP to your own database and data model, follow the Gilhari SDK documentation included in the ORMCP source distribution:

```bash
# Download the source distribution to access the full SDK
pip download --no-binary :all: \
  --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server

# Extract it
tar -xzf ormcp_server-*.tar.gz
cd ormcp_server-*/

# The Gilhari SDK is in:
# - Gilhari_SDK/          (documentation, tools, sample apps)
# - gilhari_example1/     (example microservice)
```

---

## Step 3: Configure Environment Variables

Set these variables in your terminal before starting ORMCP Server. For the example microservice running on port 80:

```bash
export GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
export MCP_SERVER_NAME="MyORMCPServer"
```

**All available configuration variables:**

| Variable | Description | Default |
|---|---|---|
| `GILHARI_BASE_URL` | Gilhari microservice URL | `http://localhost:80/gilhari/v1/` |
| `MCP_SERVER_NAME` | Server identifier | `ORMCPServerDemo` |
| `GILHARI_TIMEOUT` | API timeout in seconds | `30` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `READONLY_MODE` | Expose only read operations | `False` |
| `GILHARI_NAME` | Name of the Gilhari container | `""` |
| `GILHARI_IMAGE` | Docker image for Gilhari | `""` |
| `GILHARI_HOST` | Host IP for Gilhari | `localhost` |
| `GILHARI_PORT` | Port for Gilhari | `80` |

To make these variables permanent, add the `export` lines to your `~/.zshrc` (macOS default since Catalina) or `~/.bashrc`:

```bash
# Add to ~/.zshrc or ~/.bashrc
export GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
export MCP_SERVER_NAME="MyORMCPServer"

# Reload your shell
source ~/.zshrc   # or source ~/.bashrc
```

---

## Step 4: Start ORMCP Server

If you are using a virtual environment, activate it first:

```bash
source .venv/bin/activate
```

Then start the server:

```bash
ormcp-server
```

**Expected output:**

```
[INFO] ORMCP server name: MyORMCPServer
[INFO] GILHARI BASE URL: http://localhost:80/gilhari/v1/
[INFO] ORMCP server v0.5.x starting in stdio mode ...
```

### Alternative Start Methods

```bash
# Using the full path (if not in PATH)
~/.local/bin/ormcp-server

# Using Python directly (always works)
python -m ormcp_server

# HTTP mode (experimental)
ormcp-server --mode http --port 8080
```

---

## Step 5: Connect Your AI Client

### Claude Desktop

Locate or create your Claude Desktop config file at:

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

#### Option 1: Using the command name (virtual environment)

```json
{
  "mcpServers": {
    "my-ormcp-server": {
      "command": "/path/to/.venv/bin/ormcp-server",
      "args": [],
      "env": {
        "GILHARI_BASE_URL": "http://localhost:80/gilhari/v1/",
        "MCP_SERVER_NAME": "MyORMCPServer"
      }
    }
  }
}
```

#### Option 2: Using the command name (global install)

```json
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

#### Option 3: Using Python directly

```json
{
  "mcpServers": {
    "my-ormcp-server": {
      "command": "python",
      "args": ["-m", "ormcp_server"],
      "env": {
        "GILHARI_BASE_URL": "http://localhost:80/gilhari/v1/",
        "MCP_SERVER_NAME": "MyORMCPServer"
      }
    }
  }
}
```

To find the exact path to your `ormcp-server` executable:

```bash
which ormcp-server
# or
pip show -f ormcp-server | grep "ormcp-server$"
```

> **Note:** When using Claude Desktop, steps 3 and 4 above (setting environment variables and manually starting the server) are not necessary — Claude Desktop automatically starts the ORMCP server in STDIO mode using the config above.

### Gemini CLI

Add to your Gemini `settings.json`. Note that Gemini CLI currently requires HTTP mode, so start ORMCP with `--mode http` first:

```json
{
  "mcpServers": {
    "my-ormcp-server-http": {
      "httpUrl": "http://127.0.0.1:8080/mcp"
    }
  }
}
```

### Other MCP Clients

Configure using the appropriate transport (STDIO or HTTP) per your client's requirements. See:
- [Interacting with ORMCP Server in STDIO Mode](./Interacting_With_ORMCP_Server_In_STDIO_Mode.md)
- [Interacting with ORMCP Server in HTTP Mode](./Interacting_With_ORMCP_Server_In_HTTP_Mode.md)

---

## Troubleshooting

### `command not found: ormcp-server`

The executable is installed to `~/.local/bin/` but that directory may not be in your PATH. Add it:

```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"

# Reload
source ~/.zshrc   # or source ~/.bashrc
```

Or use the full path directly:

```bash
~/.local/bin/ormcp-server
```

### "Externally managed environment" error

Modern macOS Python installations (via Homebrew or system Python) may block global pip installs. Use a virtual environment as shown in Step 1.

### Shell script permission denied

If `./build.sh` is not executable:

```bash
chmod +x *.sh
# then re-run
./build.sh
```

### Enable debug logging

```bash
export LOG_LEVEL=DEBUG
ormcp-server
```

### Server won't start

Verify Gilhari is running and accessible:

```bash
curl -i http://localhost:80/gilhari/v1/getObjectModelSummary/now
```

For more, see the [Complete Troubleshooting Guide](./troubleshooting.md).

---

## Resources

- [Main README](../README.md) — Complete multi-platform reference
- [MCP Tools API Reference](../reference/ormcp_tools_reference.md)
- [MCP Protocol Reference](./mcp_protocol_reference.md)
- [Example Gilhari Microservice](https://github.com/SoftwareTree/gilhari_example1)
- [Bug Reports & Feedback](https://github.com/softwaretree/ormcp-docs/issues)
- Email: [ormcp_support@softwaretree.com](mailto:ormcp_support@softwaretree.com)
