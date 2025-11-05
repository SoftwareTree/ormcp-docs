Copyright (c) 2025, Software Tree

# ORMCP Server Quick Start Guide

Get up and running with ORMCP Server in minutes.

---

## Prerequisites

Before starting, ensure you have:

- **Python 3.12+** installed
- **Docker** installed and running
- **Beta access token** for Gemfury (request at [softwaretree.com/products/ormcp](https://www.softwaretree.com))

---

## Three Simple Steps

### 1. Scope Your Data

Define lightweight object models for your relevant data and write a declarative ORM specification.

**For this quick start, we'll use a pre-built example.**

### 2. Build Your Gilhari Microservice

Add models, ORM spec, and JDBC driver to a Dockerfile and build the Gilhari Docker image.

**We'll use [gilhari_example1](https://github.com/SoftwareTree/gilhari_example1) - a ready-to-use example.**

### 3. Run with ORMCP

Connect ORMCP to the Gilhari microservice and start interacting with data.

---

## Step-by-Step Setup

### Step 1: Install ORMCP Server

```bash
# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install ORMCP Server from Gemfury (Beta)
# Note: --extra-index-url is required because build dependencies (like hatchling) 
# are available on PyPI but not on Gemfury
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server
```

Replace `YOUR_TOKEN` with your beta access token.

# Verify installation:**
```bash
pip show ormcp-server
ormcp-server --help
```

**For Production Users (PyPI):**
```bash
# Install from PyPI (available after beta)
pip install ormcp-server

# Verify installation
pip show ormcp-server
```

📖 **Need help?** See the [Installation Guide](installation.md)

---

### Step 2: Set Up Gilhari Microservice

Clone and run the example Gilhari microservice:

```bash
# Clone the example repository
git clone https://github.com/SoftwareTree/gilhari_example1.git
cd gilhari_example1

# Pull Gilhari Docker image
docker pull softwaretree/gilhari:latest

# Build the example microservice
./build.sh   # Linux/Mac
# or
./build.cmd  # Windows

# Run the microservice
docker run -p 80:8081 gilhari_example1:1.0
```

**Verify it's running:**
```bash
# Test the Gilhari microservice
curl http://localhost:80/gilhari/v1/getObjectModelSummary/now
```

You should see JSON output describing the User object model.

**Optional: Populate with sample data**
```bash
# Linux/Mac
./curlCommandsPopulate.sh

# Windows
./curlCommandsPopulate.cmd
```

📖 **Need more details?** See the [Gilhari Setup Guide](gilhari_setup.md)

---

### Step 3: Configure Environment

Set environment variables to connect ORMCP to Gilhari:

**Linux/Mac:**
```bash
export GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
export MCP_SERVER_NAME="MyORMCPServer"
export LOG_LEVEL="INFO"
```

**Windows (Command Prompt):**
```cmd
set GILHARI_BASE_URL=http://localhost:80/gilhari/v1/
set MCP_SERVER_NAME=MyORMCPServer
set LOG_LEVEL=INFO
```

**Windows (PowerShell):**
```powershell
$env:GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
$env:MCP_SERVER_NAME="MyORMCPServer"
$env:LOG_LEVEL="INFO"
```

---

### Step 4: Connect Your AI Client

#### For Claude Desktop

**Find your config file:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**Add ORMCP Server configuration:**

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

**Windows users - Use full path if needed:**
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

**To find your path:**
```bash
# Windows (PowerShell)
(Get-Command ormcp-server).Source

# Linux/Mac
which ormcp-server
```

**Restart Claude Desktop** to load the configuration.

#### For Other MCP Clients

See the [Integration Guides](../docs/Interacting_With_ORMCP_Server_In_STDIO_Mode.md) for:
- Gemini CLI
- OpenAI GPTs
- Custom MCP clients

---

## Test Your Setup

### 1. Verify Connection

Open Claude Desktop and look for the tools icon (hammer) in the chat interface. You should see "MyORMCPServer" listed.

### 2. Run Your First Query

**Try this prompt in Claude:**

> "Show me all users"

**Expected behavior:**
1. Claude recognizes you want User objects
2. Calls the `query` tool with `className="User"`
3. ORMCP translates to Gilhari
4. Gilhari queries the database
5. Results return as JSON
6. Claude presents the data naturally

**Example result:**
```
Here are all the users in the database:

1. Mary55 from Campbell, CA (age 55)
2. Mike56 from Boston, MA (age 56)
3. John65 from New York, NY (age 65)
...
```

### 3. Try Filtering

> "Show me all users with age >= 55"

**Behind the scenes:**
```json
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

### 4. Try Aggregation

> "What's the average age of users in California?"

**Behind the scenes:**
```json
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

**Result:** `49`

### 5. Try Data Modification

> "Add a new user: Sarah Johnson from Seattle, WA, age 42, id 100"

**Behind the scenes:**
```json
{
  "name": "insert",
  "arguments": {
    "className": "User",
    "jsonObjects": [
      {
        "id": 100,
        "name": "Sarah Johnson",
        "city": "Seattle",
        "state": "WA",
        "age": 42
      }
    ],
    "deep": true
  }
}
```

---

## Usage Examples

### Query with Multiple Filters

**Prompt:** "Show me users from California or Massachusetts, aged 50-60"

**Generated filter:** `(state='CA' OR state='MA') AND age >= 50 AND age <= 60`

### Get Specific User

**Prompt:** "Get user with ID 55"

**Behind the scenes:**
```json
{
  "name": "getObjectById",
  "arguments": {
    "className": "User",
    "primaryKey": {"id": 55},
    "deep": true
  }
}
```

### Update Data

**Prompt:** "Update user 65: change their city to Portland"

**Behind the scenes:**
```json
{
  "name": "update",
  "arguments": {
    "className": "User",
    "jsonObjects": [
      {
        "id": 65,
        "city": "Portland"
      }
    ],
    "deep": false
  }
}
```

### Bulk Operations

**Prompt:** "Delete all users from California"

**Behind the scenes:**
```json
{
  "name": "delete2",
  "arguments": {
    "className": "User",
    "filter": "state='CA'",
    "deep": false
  }
}
```

### Statistical Queries

**Prompt:** "How many users are there in each state?"

Claude will use multiple `getAggregate` calls with different filters to build the report.

---

## Understanding the Data Flow

```
You: "Show me all users aged 55+"
  ↓
Claude: Understands intent → needs User objects with age filter
  ↓
Claude calls: query(className="User", filter="age >= 55", deep=true)
  ↓
ORMCP Server: Receives MCP tool call
  ↓
ORMCP → Gilhari: REST API call with JSON request
  ↓
Gilhari: 
  - Reads ORM specification
  - Generates SQL: SELECT * FROM users WHERE age >= 55
  - Executes query via JDBC
  - Converts rows to JSON objects
  ↓
Gilhari → ORMCP: Returns JSON objects
  ↓
ORMCP → Claude: Returns via MCP protocol
  ↓
Claude: Presents results naturally to you
```

---

## What's in the Example Database?

The `gilhari_example1` microservice includes a SQLite database with a simple User table:

**User Object Structure:**
```json
{
  "id": 55,
  "name": "Mary55",
  "city": "Campbell",
  "state": "CA",
  "age": 55
}
```

**Database Schema:**
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  name TEXT,
  city TEXT,
  state TEXT,
  age INTEGER
);
```

**Sample Data:** 50+ users across different states and age ranges.

---

## Configuration Options

### Environment Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `GILHARI_BASE_URL` | Gilhari microservice URL | `http://localhost:80/gilhari/v1/` | `http://myhost:8888/gilhari/v1/` |
| `MCP_SERVER_NAME` | Server identifier | `ORMCPServerDemo` | `MyORMCPServer` |
| `GILHARI_TIMEOUT` | API timeout (seconds) | `30` | `60` |
| `LOG_LEVEL` | Logging verbosity | `INFO` | `DEBUG`, `WARNING`, `ERROR` |
| `READONLY_MODE` | Expose only read operations | `False` | `True` |

### Read-Only Mode

To prevent data modifications:

```bash
# Linux/Mac
export READONLY_MODE="True"

# Windows
set READONLY_MODE=True
```

This disables `insert`, `update`, `update2`, `delete`, and `delete2` tools.

---

## Next Steps

### Explore More Examples

Try other Gilhari example repositories:

- **[gilhari_simple_example](https://github.com/SoftwareTree/gilhari_simple_example)** - Simple Employee objects
- **[gilhari_onetomany_example](https://github.com/SoftwareTree/gilhari_onetomany_example)** - One-to-many relationships
- **[gilhari_relationships_example](https://github.com/SoftwareTree/gilhari_relationships_example)** - Complex relationships
- **[gilhari_manytomany_example](https://github.com/SoftwareTree/gilhari_manytomany_example)** - Many-to-many relationships

### Learn More

- **[MCP Tools Reference](../reference/ormcp_tools_reference.md)** - Complete API documentation
- **[Gilhari Setup Guide](gilhari_setup.md)** - Create your own microservice
- **[Integration Guides](../docs/Interacting_With_ORMCP_Server_In_STDIO_Mode.md)** - Other MCP clients
- **[Client Example](../client/using_ormcp_client_example.md)** - Python client tutorial

### Build Your Own

1. **Define your domain model** - What objects does your application need?
2. **Create ORM specification** - Map objects to database tables
3. **Build Gilhari microservice** - Package everything in Docker
4. **Connect ORMCP** - Point to your new microservice
5. **Start querying** - Use natural language with your data

---

## Troubleshooting

### ORMCP won't start

**Check Gilhari is running:**
```bash
curl http://localhost:80/gilhari/v1/getObjectModelSummary/now
```

**Verify environment variables:**
```bash
# Linux/Mac
echo $GILHARI_BASE_URL

# Windows
echo %GILHARI_BASE_URL%
```

### Claude doesn't see tools

1. **Restart Claude Desktop** after changing config
2. **Check config file syntax** - Ensure valid JSON (no trailing commas)
3. **Verify path** - Use full path to ormcp-server executable
4. **Check logs** - Look in Claude Desktop developer console

### Queries fail

1. **Verify class names** - Check `getObjectModelSummary` output
2. **Check filter syntax** - Use SQL-like WHERE clause syntax
3. **Review Gilhari logs** - Check Docker container logs
4. **Enable debug mode** - Set `LOG_LEVEL=DEBUG`

📖 **[Complete Troubleshooting Guide](troubleshooting.md)**

---

## Support

- **Documentation:** [ormcp-docs repository](https://github.com/softwaretree/ormcp-docs)
- **Issues:** [Report a problem](https://github.com/softwaretree/ormcp-docs/issues)
- **Email:** ormcp_support@softwaretree.com

---

## Related Documentation

- [Back to Main README](../README.md)
- [Installation Guide](installation.md)
- [Gilhari Setup Guide](gilhari_setup.md)
- [Troubleshooting Guide](troubleshooting.md)
- [MCP Tools Reference](../reference/ormcp_tools_reference.md)