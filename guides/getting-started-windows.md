# Getting Started with ORMCP Server on Windows

> **Platform-specific guide** — This page consolidates all Windows instructions in one place.
> For the complete multi-platform reference, see the [main README](../README.md).

---

## Prerequisites

- **Python 3.12+** — Check your version: `python --version`
- **Docker** — Required for the Gilhari microservice. [Get Docker](https://docs.docker.com/get-docker/) if not already installed.
- **JDBC driver** for your target database (bundled in the Gilhari SDK)

---

## Step 1: Install ORMCP Server

### Recommended: Virtual Environment

Using a virtual environment keeps your installation clean and avoids conflicts with other Python projects.

**Command Prompt:**

```cmd
REM Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

REM Install ORMCP Server (Beta — replace YOUR_TOKEN with your beta access token)
REM Note: --extra-index-url is required because build dependencies (like hatchling)
REM are available on PyPI but not on Gemfury
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ ^
  --extra-index-url https://pypi.org/simple ^
  ormcp-server

REM Verify installation
pip show ormcp-server
```

**PowerShell:**

```powershell
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install ORMCP Server (Beta — replace YOUR_TOKEN with your beta access token)
# Note: --extra-index-url is required because build dependencies (like hatchling)
# are available on PyPI but not on Gemfury
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ `
  --extra-index-url https://pypi.org/simple `
  ormcp-server

# Verify installation
pip show ormcp-server
```

Request your beta access token at [softwaretree.com/products/ormcp](https://www.softwaretree.com/products/ormcp).

> **Production (after beta):** `pip install ormcp-server`

### Global Installation (Optional)

For a global install without a virtual environment, the `ormcp-server` executable is placed in your Python Scripts directory (e.g., `%APPDATA%\Python\Python313\Scripts\`). If the command is not found after installation, add that directory to your PATH (see [Troubleshooting](#troubleshooting) below).

**Command Prompt:**

```cmd
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ ^
  --extra-index-url https://pypi.org/simple ^
  ormcp-server
```

**PowerShell:**

```powershell
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ `
  --extra-index-url https://pypi.org/simple `
  ormcp-server
```

---

## Step 2: Set Up the Gilhari Microservice

ORMCP Server depends on **Gilhari**, a microservice that handles the ORM and database communication. You must have it running before starting ORMCP.

### Pull the Gilhari Docker Image

```cmd
docker pull softwaretree/gilhari:latest
```

### Run the Example Microservice (Quickest Path)

A ready-to-use example microservice is available in a separate repository:

```cmd
REM Clone the example (manages User objects against a SQLite database)
git clone https://github.com/SoftwareTree/gilhari_example1.git
cd gilhari_example1

REM Build the Docker image
build.cmd

REM Run the microservice (listens on port 80)
docker run -p 80:8081 gilhari_example1:1.0

REM (Optional) Populate the database with sample data
curlCommandsPopulate.cmd
```

### Build Your Own Gilhari Microservice

To connect ORMCP to your own database and data model, follow the Gilhari SDK documentation included in the ORMCP source distribution:

**Command Prompt:**

```cmd
REM Download the source distribution to access the full SDK
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ ^
  --extra-index-url https://pypi.org/simple ^
  ormcp-server

REM Extract the .tar.gz file
REM If you have tar available (Windows 10+):
tar -xzf ormcp_server-*.tar.gz
cd ormcp_server-*\

REM Alternative: use 7-Zip or WinRAR to extract the .tar.gz file
```

The extracted package contains:
- `Gilhari_SDK/` — documentation, tools, and sample apps
- `gilhari_example1/` — example microservice
- `package/client/` — example client code
- `package/docs/` — additional documentation

---

## Step 3: Configure Environment Variables

Set these variables before starting ORMCP Server. For the example microservice running on port 80:

**Command Prompt:**

```cmd
set GILHARI_BASE_URL=http://localhost:80/gilhari/v1/
set MCP_SERVER_NAME=MyORMCPServer
```

**PowerShell:**

```powershell
$env:GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
$env:MCP_SERVER_NAME="MyORMCPServer"
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

To make these variables permanent across sessions, use `setx` in Command Prompt (takes effect in new terminals):

```cmd
setx GILHARI_BASE_URL "http://localhost:80/gilhari/v1/"
setx MCP_SERVER_NAME "MyORMCPServer"
```

Or set them via **System Properties → Advanced → Environment Variables** in the Windows control panel.

---

## Step 4: Start ORMCP Server

If you are using a virtual environment, activate it first:

**Command Prompt:**

```cmd
.venv\Scripts\activate
```

**PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

Then start the server:

```cmd
ormcp-server
```

**Expected output:**

```
[INFO] ORMCP server name: MyORMCPServer
[INFO] GILHARI BASE URL: http://localhost:80/gilhari/v1/
[INFO] ORMCP server v0.5.x starting in stdio mode ...
```

### Alternative Start Methods

```cmd
REM Using the full path (if not in PATH)
%APPDATA%\Python\Python313\Scripts\ormcp-server.exe

REM Using Python directly (always works)
python -m ormcp_server

REM HTTP mode (experimental)
ormcp-server --mode http --port 8080
```

---

## Step 5: Connect Your AI Client

### Claude Desktop

Locate or create your Claude Desktop config file at:

```
%APPDATA%\Claude\claude_desktop_config.json
```

#### Option 1: Using the full path (recommended)

Using the full path to the executable is the most reliable option on Windows and avoids PATH-related issues:

```json
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

Replace `<YourUsername>` with your actual Windows username. To find your exact path:

```powershell
# PowerShell
(Get-Command ormcp-server).Source

# Command Prompt
where ormcp-server

# Any terminal
pip show -f ormcp-server | findstr "ormcp-server.exe"
```

#### Option 2: Using a virtual environment path

If you installed into a virtual environment:

```json
{
  "mcpServers": {
    "my-ormcp-server": {
      "command": "C:\\path\\to\\your\\.venv\\Scripts\\ormcp-server.exe",
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

### OpenAI GPTs (Developer Mode)

The ORMCP server must be running in HTTP mode and accessible via a public URL. See the [main README](../README.md#openai-gpts-developer-mode) for the full walkthrough using `cloudflared` or `ngrok`.

### Other MCP Clients

Configure using the appropriate transport (STDIO or HTTP) per your client's requirements. See:
- [Interacting with ORMCP Server in STDIO Mode](./Interacting_With_ORMCP_Server_In_STDIO_Mode.md)
- [Interacting with ORMCP Server in HTTP Mode](./Interacting_With_ORMCP_Server_In_HTTP_Mode.md)

---

## Troubleshooting

### `'ormcp-server' is not recognized`

The Python Scripts directory is not in your PATH. Fix it with one of these options:

**Option 1: Add to PATH permanently (Command Prompt, then restart terminal):**

```cmd
setx PATH "%PATH%;%APPDATA%\Python\Python313\Scripts"
```

**Option 2: Use the full path directly:**

```cmd
%APPDATA%\Python\Python313\Scripts\ormcp-server.exe
```

**Option 3: Use Python directly (no PATH change needed):**

```cmd
python -m ormcp_server
```

> **Note:** The exact Scripts path depends on your Python version. Replace `Python313` with your version (e.g., `Python312`). Find it with: `pip show -f ormcp-server | findstr "Location"`

### Enable debug logging

**Command Prompt:**

```cmd
set LOG_LEVEL=DEBUG
ormcp-server
```

**PowerShell:**

```powershell
$env:LOG_LEVEL="DEBUG"
ormcp-server
```

### Server won't start

Verify Gilhari is running and accessible:

```cmd
curl -i http://localhost:80/gilhari/v1/getObjectModelSummary/now
```

### Extracting `.tar.gz` without third-party tools

Windows 10 and later include `tar` in PowerShell and Command Prompt:

```cmd
tar -xzf ormcp_server-0.4.x.tar.gz
```

For older Windows versions, use [7-Zip](https://www.7-zip.org/) or [WinRAR](https://www.rarlab.com/) to extract the file.

For more, see the [Complete Troubleshooting Guide](./troubleshooting.md).

---

## Resources

- [Main README](../README.md) — Complete multi-platform reference
- [MCP Tools API Reference](../reference/ormcp_tools_reference.md)
- [MCP Protocol Reference](./mcp_protocol_reference.md)
- [Example Gilhari Microservice](https://github.com/SoftwareTree/gilhari_example1)
- [Bug Reports & Feedback](https://github.com/softwaretree/ormcp-docs/issues)
- Email: [ormcp_support@softwaretree.com](mailto:ormcp_support@softwaretree.com)
