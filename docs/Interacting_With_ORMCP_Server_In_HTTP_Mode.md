Copyright (c) 2025, Software Tree

# Interacting with ORMCP Server in HTTP Mode - User Guide

This guide explains how to interact with an ORMCP server running in HTTP mode using curl or other HTTP clients.

## Prerequisites

When your ORMCP server starts in HTTP mode, you'll see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

## Step-by-Step Connection Process

### 1. Initialize the Connection

First, establish a connection and initialize the MCP session:

```bash
curl -X POST \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl-client","version":"1.0.0"}}}' \
  "http://127.0.0.1:8080/mcp/"
```

**Key Points:**
- Use the `/mcp/` endpoint (with trailing slash)
- Include both `application/json` and `text/event-stream` in Accept header
- The server will return a session ID in the `mcp-session-id` header

**Expected Response:**
```
event: message
data: {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{"listChanged":false},...},"serverInfo":{"name":"ORMCPServerDemo","version":"1.9.4"}}}
```

Save the `mcp-session-id` from the response headers (e.g., `c97b99b7b9b343bd8cf590f5d5a40367`).

### 2. Send Initialized Notification

After successful initialization, send the required initialized notification:

```bash
curl -X POST \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -H "mcp-session-id: YOUR_SESSION_ID_HERE" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  "http://127.0.0.1:8080/mcp/"
```

**Note:** This request has no `id` field since it's a notification, not a request expecting a response.

### 3. List Available Tools

Now you can discover what tools are available:

```bash
curl --max-time 10 \
  -X POST \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -H "mcp-session-id: YOUR_SESSION_ID_HERE" \
  -d '{"jsonrpc":"2.0","id":"2","method":"tools/list"}' \
  "http://127.0.0.1:8080/mcp/"
```

### 4. Call Tools

Use the `tools/call` method to execute available tools:

```bash
curl --max-time 10 \
  -X POST \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -H "mcp-session-id: YOUR_SESSION_ID_HERE" \
  -d '{"jsonrpc":"2.0","id":"3","method":"tools/call","params":{"name":"TOOL_NAME","arguments":{"param1":"value1"}}}' \
  "http://127.0.0.1:8080/mcp/"
```

## Available Methods

| Method | Description | Example Usage |
|--------|-------------|---------------|
| `tools/list` | List all available tools | See step 3 above |
| `tools/call` | Execute a specific tool | See step 4 above |
| `resources/list` | List available resources | Similar to tools/list |
| `prompts/list` | List available prompts | Similar to tools/list |

## Common Issues and Solutions

### Issue: "Not Acceptable: Client must accept text/event-stream"
**Solution:** Include both content types in Accept header:
```
-H "Accept: application/json, text/event-stream"
```

### Issue: "Bad Request: Missing session ID"
**Solution:** 
1. Ensure you've initialized first and captured the session ID
2. Include the session ID in subsequent requests:
```
-H "mcp-session-id: YOUR_SESSION_ID_HERE"
```

### Issue: "Invalid request parameters"
**Solution:** Send the `notifications/initialized` notification after initialization but before making other requests.

### Issue: Commands hanging with ping messages
This is normal for Server-Sent Events. Use `--max-time 10` to set a timeout, or press `Ctrl+C` to cancel.

## Browser Alternative

For browser-based interaction, you can use JavaScript:

```javascript
// Initialize
fetch('http://127.0.0.1:8080/mcp/', {
  method: 'POST',
  headers: {
    'Accept': 'application/json, text/event-stream',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    "jsonrpc": "2.0",
    "id": "1",
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "browser-client", "version": "1.0.0"}
    }
  })
})
.then(response => {
  const sessionId = response.headers.get('mcp-session-id');
  // Use sessionId for subsequent requests
});
```

## Windows Command Line Notes

- Use double quotes for JSON strings and escape inner quotes with `\"`
- Use single-line commands to avoid copy-paste issues
- Add `--max-time 10` to prevent hanging connections

This completes the basic interaction pattern with your MCP server in HTTP mode.