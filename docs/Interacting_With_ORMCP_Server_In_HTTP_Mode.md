Copyright (c) 2025, Software Tree

# Interacting with ORMCP Server in HTTP Mode - User Guide

This guide explains how to interact with an ORMCP server running in HTTP mode using curl or other HTTP clients.

## Prerequisites

Start ORMCP Server in HTTP mode (the Gilhari microservice must already be running at `GILHARI_BASE_URL`, otherwise ORMCP stops at start-up with a message naming the address it checked):

```bash
ormcp-server --transport http --port 8080
```

When it is ready, you'll see output like:
```
🟢 ORMCP server v0.7.x starting in HTTP mode on 127.0.0.1:8080...
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

## Step-by-Step Connection Process

### 1. Initialize the Connection

First, establish a connection and initialize the MCP session:

```bash
curl -X POST \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":"1","method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl-client","version":"1.0.0"}}}' \
  "http://127.0.0.1:8080/mcp"
```

**Key Points:**
- Use the `/mcp` endpoint, without a trailing slash (`/mcp/` answers with a `307` redirect, which `curl -X POST` does not follow)
- Include both `application/json` and `text/event-stream` in Accept header
- The server will return a session ID in the `mcp-session-id` header

**Expected Response** (shortened):
```
event: message
data: {"jsonrpc":"2.0","id":"1","result":{"protocolVersion":"2025-06-18","capabilities":{"tools":{"listChanged":true},...},"serverInfo":{"name":"ORMCPServerDemo","version":"0.7.x"},"instructions":"..."}}
```

`serverInfo.version` is the ORMCP Server version (since 0.7.0).

Save the `mcp-session-id` from the response headers (e.g., `c97b99b7b9b343bd8cf590f5d5a40367`).

### 2. Send Initialized Notification

After successful initialization, send the required initialized notification:

```bash
curl -X POST \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -H "mcp-session-id: YOUR_SESSION_ID_HERE" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  "http://127.0.0.1:8080/mcp"
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
  "http://127.0.0.1:8080/mcp"
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
  "http://127.0.0.1:8080/mcp"
```

A successful call returns the tool's output as text in `result.content` (and again in `result.structuredContent.result`), with `"isError": false`. A failing call also returns a `result`, with `"isError": true` and the error message as text — for example:

```
data: {"jsonrpc":"2.0","id":"3","result":{"content":[{"type":"text","text":"Error calling tool 'query': HTTP 404: Error during query: ..."}],"isError":true}}
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

### Issue: `307 Temporary Redirect`
**Solution:** Use `/mcp` without a trailing slash.

### Issue: `421 Misdirected Request`
**Cause:** ORMCP's Host/Origin protection (on by default) rejects requests whose `Host` header is not trusted — for example when ORMCP is reached through a tunnel, a proxy or a Docker host name.
**Solution:** Add the host name to `ALLOWED_HOSTS` (comma-separated) before starting ORMCP, e.g. `ALLOWED_HOSTS=host.docker.internal`. See the [Troubleshooting Guide](../guides/troubleshooting.md#http-mode-421-misdirected-request).

### Issue: Commands hanging with ping messages
This is normal for Server-Sent Events. Use `--max-time 10` to set a timeout, or press `Ctrl+C` to cancel.

## Browser Alternative

For browser-based interaction, you can use JavaScript:

```javascript
// Initialize
fetch('http://127.0.0.1:8080/mcp', {
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
      "protocolVersion": "2025-06-18",
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

Note: a page served from another origin is also subject to ORMCP's Origin check; add that origin to `ALLOWED_ORIGINS` if needed.

## Windows Command Line Notes

- The Command Prompt does not accept single quotes or `\` line continuations: put each command on one line, use double quotes around the JSON, and escape the inner quotes with `\"`
- Add `--max-time 10` to prevent hanging connections

For example, the initialize request in the Command Prompt (`-i` shows the response headers, including `mcp-session-id`):

```
curl -i -X POST http://127.0.0.1:8080/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\",\"params\":{\"protocolVersion\":\"2025-06-18\",\"capabilities\":{},\"clientInfo\":{\"name\":\"curl\",\"version\":\"1\"}}}"
```

This completes the basic interaction pattern with your MCP server in HTTP mode.