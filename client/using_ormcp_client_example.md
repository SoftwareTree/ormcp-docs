# Using the ORMCP Client Example

The `ormcp_client_example.py` script demonstrates how to connect to ORMCP Server using both STDIO and HTTP transport modes. This example is useful for:

- Learning how to build MCP clients
- Testing ORMCP Server functionality
- Understanding different transport modes
- Prototyping integrations

## Prerequisites

Before running the client example, ensure you have:

1. **ORMCP Server installed:**
   ```bash
   pip install ormcp-server
   ```

2. **Gilhari microservice running:**
   - See the [Gilhari Setup Guide](../README.md#gilhari-microservice-setup)
   - Example: [gilhari_example1](https://github.com/SoftwareTree/gilhari_example1)
   ```bash
   docker run -p 80:8081 gilhari_example1:1.0
   ```

3. **Environment configured:**
   ```bash
   # Linux/Mac
   export GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
   
   # Windows (Command Prompt)
   set GILHARI_BASE_URL=http://localhost:80/gilhari/v1/
   
   # Windows (PowerShell)
   $env:GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"
   ```

## Getting the Client Example

The client example is included in the ORMCP Server source distribution:

```bash
# Download source distribution
pip download --no-binary :all: ormcp-server

# Extract it
tar -xzf ormcp_server-*.tar.gz
cd ormcp_server-*/client/

# Or download from GitHub
# (Available in ormcp-docs repository client/ directory)
```

## Running in STDIO Mode (Recommended)

STDIO mode is the simplest way to test ORMCP Server locally.

```bash
# Using default server command
python ormcp_client_example.py --mode stdio --demo

# Using custom server command
python ormcp_client_example.py --mode stdio --server_cmd "ormcp-server" --demo

# Connect to already running server by PID
python ormcp_client_example.py --mode stdio --server_pid 12345 --demo
```

### When to Use STDIO Mode

- ✅ **Testing locally** - Quick setup, no network configuration
- ✅ **Desktop integrations** - Like Claude Desktop, which uses STDIO
- ✅ **Single-user scenarios** - Simple process communication
- ✅ **Development** - Fast iteration and debugging

### How STDIO Mode Works

1. The client launches ORMCP Server as a subprocess
2. Communication happens via stdin/stdout streams
3. No network sockets, no HTTP servers needed
4. JSON-RPC messages are exchanged line-by-line

### STDIO Mode Output

```
🔌 Starting MCP server with command: ormcp-server
🟢 Server started and running in the background...
✅ Server initialized successfully

🎯 Starting demo session...

🔧 Listing available tools...
📋 Found 9 tool(s):
  1. getObjectModelSummary - Get information about the underlying object model...
  2. query - Query all qualifying objects...
  
🎮 Trying to call some tools...

--- Calling getObjectModelSummary ---
📤 Sending: {"jsonrpc":"2.0","id":2,"method":"tools/call",...}
📥 Received: {"jsonrpc":"2.0","id":2,"result":{...}}
✅ Tool result: {...}

Demo completed successfully!
```

## Running in HTTP Mode (Experimental)

HTTP mode allows ORMCP Server to run as a standalone web service.

### Step 1: Start ORMCP Server in HTTP Mode

In one terminal window:

```bash
ormcp-server --mode http --port 8080
```

Or:

```bash
python -m ormcp_server --mode http --port 8080
```

You should see:

```
[INFO] ORMCP server v0.4.3 starting in http mode...
[INFO] Server running at http://127.0.0.1:8080
```

### Step 2: Run the Client

In another terminal window:

```bash
python ormcp_client_example.py --mode http --url http://127.0.0.1:8080 --demo
```

### When to Use HTTP Mode

- ✅ **Multi-user scenarios** - Multiple clients connecting simultaneously
- ✅ **Web-based integrations** - Browser or web application clients
- ✅ **Remote access** - Connect from different machines
- ✅ **Testing HTTP transport** - When your target platform uses HTTP/SSE

### How HTTP Mode Works

1. ORMCP Server runs as a standalone HTTP service
2. Client connects via HTTP to the `/mcp` endpoint
3. The client automatically:
   - Adds `/mcp/` to the URL if needed
   - Manages session tokens
   - Handles Server-Sent Events (SSE) responses
   - Sends required MCP protocol notifications

### HTTP Mode Output

```
✅ Successfully connected to http://127.0.0.1:8080/mcp/
📋 Session ID: abc123def456

🎯 Starting demo session...

🔧 Listing available tools...
📤 Sending HTTP: {"jsonrpc":"2.0","id":1,"method":"tools/list"}
📥 Received HTTP: {"jsonrpc":"2.0","id":1,"result":{...}}
📋 Found 9 tool(s)

Demo completed successfully!
```

## What the Demo Does

The `--demo` flag runs an automated demonstration session:

### 1. Connection Initialization
- Establishes connection (stdio or HTTP)
- Sends `initialize` request with protocol version `2024-11-05`
- Sends `initialized` notification
- Confirms connection is ready

### 2. List Available Tools
- Calls `tools/list` method
- Displays all available tools with descriptions
- Shows you what operations ORMCP Server supports

### 3. List Available Resources
- Calls `resources/list` method  
- Shows any resources exposed by the server
- Resources are typically read-only data endpoints

### 4. Automated Tool Calls
- Automatically calls the first 3 tools from the list
- Generates demo arguments based on tool schemas:
  - Integers: Uses `42` for numeric fields, `10` for others
  - Strings: Uses `"demo_object"` for name fields, `""` for filters
  - Booleans: Uses `True`
  - Arrays/Objects: Uses empty `[]` or `{}`
- Adds 1-second delay between calls

### 5. Display Results
- Shows JSON-RPC request messages sent
- Shows JSON-RPC response messages received  
- Pretty-prints tool results with indentation
- Reports success or failure for each operation

## Customizing the Example

You can modify `ormcp_client_example.py` or use it programmatically:

### Using as a Python Module

```python
from ormcp_client_example import MCPClient

# Create client
client = MCPClient()

# Option 1: STDIO mode with server command
server_cmd = ["ormcp-server"]
if client.connect_stdio(server_cmd):
    # List tools
    tools = client.list_tools()
    
    # Call a tool
    result = client.call_tool("query", {
        "className": "User",
        "filter": "age >= 30",
        "maxObjects": 10,
        "deep": False
    })
    print(result)
    
    # Close connection
    client.close()

# Option 2: HTTP mode
client2 = MCPClient()
if client2.connect_http("http://127.0.0.1:8080"):
    # Make tool calls
    result = client2.call_tool("getObjectModelSummary", {})
    print(result)
    
    client2.close()
```

### Example: Query with Custom Arguments

```python
# Query users in Boston over 30, ordered by name
result = client.call_tool("query", {
    "className": "User",
    "filter": "age >= 30 AND city='Boston' ORDER BY name",
    "maxObjects": 5,
    "deep": False
})
```

### Example: Get Object by ID

```python
# Retrieve specific user
user = client.call_tool("getObjectById", {
    "className": "User",
    "primaryKey": {"id": 123},
    "deep": True
})
```

### Example: Calculate Statistics

```python
# Average age of all users
avg_age = client.call_tool("getAggregate", {
    "className": "User",
    "attributeName": "age",
    "aggregateType": "AVG",
    "filter": ""
})

# Count users in California
ca_count = client.call_tool("getAggregate", {
    "className": "User",
    "attributeName": "id",
    "aggregateType": "COUNT",
    "filter": "state='CA'"
})
```

### Example: Insert Data

```python
# Create new user
result = client.call_tool("insert", {
    "className": "User",
    "jsonObjects": [
        {
            "id": 999,
            "name": "Test User",
            "age": 25,
            "city": "San Francisco",
            "state": "CA"
        }
    ],
    "deep": True
})
```

### Example: Update Data

```python
# Update existing user
result = client.call_tool("update", {
    "className": "User",
    "jsonObjects": [
        {
            "id": 999,
            "name": "Updated Name",
            "age": 26
        }
    ],
    "deep": False
})
```

### Example: Delete Data

```python
# Delete user by ID
result = client.call_tool("delete", {
    "className": "User",
    "jsonObjects": [
        {"id": 999}
    ],
    "deep": False
})
```

## Advanced Usage

### Command Line Options

The client supports several command-line options:

```bash
# Full options list
python ormcp_client_example.py \
    --mode [stdio|http] \
    --server_cmd "command to start server" \
    --server_pid PID \
    --url http://127.0.0.1:8080 \
    --demo

# STDIO mode options

# 1. Start new server with default command
python ormcp_client_example.py --mode stdio --demo

# 2. Start new server with custom command
python ormcp_client_example.py --mode stdio --server_cmd "ormcp-server" --demo

# 3. Connect to already running server by PID
python ormcp_client_example.py --mode stdio --server_pid 12345 --demo

# HTTP mode options

# Default URL (http://127.0.0.1:8080)
python ormcp_client_example.py --mode http --demo

# Custom URL
python ormcp_client_example.py --mode http --url http://localhost:9000 --demo
```

**Available Arguments:**

- `--mode` - Connection mode: `stdio` or `http` (default: `stdio`)
- `--server_cmd` - Command to start MCP server for stdio mode (has a default)
- `--server_pid` - Connect to existing MCP server by process ID
- `--url` - URL of HTTP MCP server (default: `http://127.0.0.1:8080`)
- `--demo` - Run automated demo session (list and call tools)

### Without Demo Mode (Interactive)

Run the client without `--demo` flag for interactive mode:

```bash
# STDIO mode - interactive
python ormcp_client_example.py --mode stdio

# HTTP mode - interactive  
python ormcp_client_example.py --mode http --url http://127.0.0.1:8080
```

**Interactive Commands:**

Once in interactive mode, you can use these commands:

```
> tools                                    # List available tools
> resources                                # List available resources
> call <tool_name> <args_json>            # Call a tool with JSON arguments
> read <resource_uri>                     # Read a resource
> quit                                     # Exit the client

# Examples:
> tools
> call query {"className": "User", "filter": "", "maxObjects": 5}
> call getObjectById {"className": "User", "primaryKey": {"id": 1}}
> call getAggregate {"className": "User", "attributeName": "age", "aggregateType": "AVG"}
> quit
```

### Environment Variables

```bash
# Gilhari connection
export GILHARI_BASE_URL="http://localhost:80/gilhari/v1/"

# ORMCP configuration
export MCP_SERVER_NAME="MyORMCPServer"
export LOG_LEVEL="DEBUG"
export READONLY_MODE="False"

# Run client
python ormcp_client_example.py --mode stdio --demo
```

## Troubleshooting

### Connection Refused

**Problem:** `Connection refused` or `Unable to connect to server`

**Solutions:**

1. **Verify Gilhari is running:**
   ```bash
   curl http://localhost:80/gilhari/v1/getObjectModelSummary/now
   ```

2. **Check GILHARI_BASE_URL:**
   ```bash
   # Linux/Mac
   echo $GILHARI_BASE_URL
   
   # Windows
   echo %GILHARI_BASE_URL%
   ```

3. **For HTTP mode, ensure ORMCP Server is running:**
   ```bash
   # Check if port 8080 is in use
   netstat -an | grep 8080  # Linux/Mac
   netstat -an | findstr 8080  # Windows
   ```

### Tool Call Failures

**Problem:** `Tool execution failed` or `Class not found`

**Solutions:**

1. **Verify class names match your object model:**
   ```bash
   curl http://localhost:80/gilhari/v1/getObjectModelSummary/now
   ```

2. **Check attribute names and types**

3. **Review filter syntax** (SQL-like WHERE clause)

4. **Ensure primary key values are correct**

### STDIO Mode Issues

**Problem:** Subprocess fails to start

**Solutions:**

1. **Verify ORMCP Server is installed:**
   ```bash
   pip show ormcp-server
   ```

2. **Check the server command:**
   ```bash
   # Test the command manually first
   ormcp-server
   ```

3. **Use custom server command:**
   ```bash
   python ormcp_client_example.py --mode stdio --server_cmd "python -m ormcp_server" --demo
   ```

4. **Check for error messages:**
   - The client displays server stderr output with 🛑 prefix
   - Look for error messages from the server startup

**Problem:** "No process available" or stdin/stdout errors

**Solutions:**

1. **Increase initialization wait time** - Edit the code to wait longer than 2 seconds
2. **Check server actually started** - Look for server initialization messages
3. **Try connecting to existing server:**
   ```bash
   # Start server separately
   ormcp-server
   
   # In another terminal, get the PID
   ps aux | grep ormcp-server  # Linux/Mac
   tasklist | findstr ormcp    # Windows
   
   # Connect to it
   python ormcp_client_example.py --mode stdio --server_pid <PID> --demo
   ```

### HTTP Mode Issues

**Problem:** SSE connection failures or timeout errors

**Solutions:**

1. **Verify HTTP server is running:**
   ```bash
   curl http://127.0.0.1:8080/mcp
   ```

2. **Check firewall settings** - Allow port 8080

3. **Try different port:**
   ```bash
   # Server
   ormcp-server --mode http --port 9000
   
   # Client
   python ormcp_client_example.py --mode http --url http://127.0.0.1:9000 --demo
   ```

### Debugging

The client provides detailed logging output:

**Message Tracking:**
- 📤 **Sending** - Shows outgoing JSON-RPC messages
- 📥 **Received** - Shows incoming JSON-RPC responses
- 🛑 **Server STDERR** - Shows server error/log messages
- 📋 **Session ID** - Shows HTTP session tracking (HTTP mode only)

**Enable more logging:**

```bash
# Server-side logging
export LOG_LEVEL=DEBUG  # Linux/Mac
set LOG_LEVEL=DEBUG     # Windows

# Then run client
python ormcp_client_example.py --mode stdio --demo
```

**What you'll see:**

```
📤 Sending: {"jsonrpc":"2.0","id":1,"method":"initialize",...}
📥 Received: {"jsonrpc":"2.0","id":1,"result":{...}}
✅ Server initialized successfully
📋 Session ID: abc123def456  (HTTP mode only)
🛑 Server STDERR: [INFO] ORMCP server starting...
```

**Understanding Output:**
- ✅ (green check) - Successful operation
- ❌ (red X) - Failed operation or error
- 🔌 - Connection events
- 🟢 - Server started
- 🔴 - Server stopped
- 🔧 - Tool listing
- 🛠️ - Tool call
- 📚 - Resource listing

## See Also

- [MCP Protocol Reference](../docs/mcp_protocol_reference.md) - Low-level protocol details
- [MCP Tools API Reference](../reference/ormcp_tools_reference.md) - Complete tool documentation
- [Interacting with ORMCP Server in STDIO Mode](../docs/Interacting_With_ORMCP_Server_In_STDIO_Mode.md)
- [Interacting with ORMCP Server in HTTP Mode](../docs/Interacting_With_ORMCP_Server_In_HTTP_Mode.md)

## Next Steps

1. **Explore the code** - Read through `ormcp_client_example.py` to understand the implementation
2. **Modify the demo** - Add your own tool calls and test scenarios
3. **Build your integration** - Use this example as a template for your own MCP client
4. **Test different modes** - Compare STDIO vs HTTP for your use case
5. **Try with your data** - Use your own Gilhari microservice and domain model

For questions or issues, contact [ormcp_support@softwaretree.com](mailto:ormcp_support@softwaretree.com)
