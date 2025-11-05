Copyright (c) 2025, Software Tree

# MCP Protocol Reference

This guide shows the low-level JSON-RPC messages used when interacting with ORMCP Server in STDIO mode. This is useful for:

- Understanding the MCP protocol at a deeper level
- Building custom MCP clients
- Debugging connection issues
- Testing ORMCP Server manually

## Overview

The Model Context Protocol (MCP) uses JSON-RPC 2.0 for communication. When connecting to ORMCP Server in STDIO mode, messages are exchanged via standard input/output streams.

## Connection Sequence

When establishing a connection to ORMCP Server, send these messages in the following order:

### 1. Initialize Connection

Send an `initialize` request to establish the connection and negotiate protocol capabilities.

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "roots": {
        "listChanged": true
      },
      "sampling": {}
    },
    "clientInfo": {
      "name": "python-mcp-client",
      "version": "1.0.0"
    }
  }
}
```

**Expected Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "ORMCPServerDemo",
      "version": "0.4.3"
    }
  }
}
```

### 2. Send Initialized Notification

After receiving the initialize response, send an `initialized` notification to confirm the connection is ready.

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

**Note:** This is a notification (no `id` field), so no response is expected.

### 3. List Available Tools

Request the list of tools (operations) provided by ORMCP Server.

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/list"
}
```

**Expected Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "tools": [
      {
        "name": "getObjectModelSummary",
        "description": "Get information about the underlying object model...",
        "inputSchema": {...}
      },
      {
        "name": "query",
        "description": "Query all qualifying objects...",
        "inputSchema": {...}
      },
      ...
    ]
  }
}
```

## Making Tool Calls

Once the connection is established, you can call any of the available tools.

### General Template

```json
{
  "jsonrpc": "2.0",
  "id": <unique_request_id>,
  "method": "tools/call",
  "params": {
    "name": "<tool_name>",
    "arguments": {
      <tool-specific arguments>
    }
  }
}
```

### Example 1: Get Object Model Summary

Retrieve information about the database schema and available object types.

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "getObjectModelSummary",
    "arguments": {}
  }
}
```

**Expected Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\n  \"classes\": [\n    {\n      \"name\": \"User\",\n      \"attributes\": [...],\n      \"primaryKey\": [\"id\"]\n    }\n  ]\n}"
      }
    ]
  }
}
```

### Example 2: Query Objects

Query objects of a specific type with optional filtering.

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "query",
    "arguments": {
      "className": "User",
      "filter": "age >= 30",
      "maxObjects": 10,
      "deep": true
    }
  }
}
```

**Expected Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[{\"id\": 1, \"name\": \"John Doe\", \"age\": 35}, ...]"
      }
    ]
  }
}
```

### Example 3: Get Object By ID

Retrieve a specific object by its primary key.

```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "tools/call",
  "params": {
    "name": "getObjectById",
    "arguments": {
      "className": "User",
      "primaryKey": {"id": 123},
      "deep": false
    }
  }
}
```

### Example 4: Query with Filtering and Sorting

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "query",
    "arguments": {
      "className": "User",
      "filter": "city='Boston' ORDER BY name",
      "maxObjects": -1,
      "deep": false
    }
  }
}
```

### Example 5: Aggregate Data

Calculate aggregate values like COUNT, SUM, AVG, MIN, or MAX.

```json
{
  "jsonrpc": "2.0",
  "id": 8,
  "method": "tools/call",
  "params": {
    "name": "getAggregate",
    "arguments": {
      "className": "User",
      "attributeName": "age",
      "aggregateType": "AVG",
      "filter": "state='CA'"
    }
  }
}
```

### Example 6: Insert Objects

Create new objects in the database.

```json
{
  "jsonrpc": "2.0",
  "id": 9,
  "method": "tools/call",
  "params": {
    "name": "insert",
    "arguments": {
      "className": "User",
      "jsonObjects": [
        {
          "id": 100,
          "name": "Jane Smith",
          "age": 28,
          "city": "San Francisco",
          "state": "CA"
        }
      ],
      "deep": true
    }
  }
}
```

### Example 7: Update Objects

Update existing objects with new values.

```json
{
  "jsonrpc": "2.0",
  "id": 10,
  "method": "tools/call",
  "params": {
    "name": "update",
    "arguments": {
      "className": "User",
      "jsonObjects": [
        {
          "id": 100,
          "name": "Jane Smith-Johnson",
          "age": 29
        }
      ],
      "deep": false
    }
  }
}
```

### Example 8: Delete Objects

Delete specific objects from the database.

```json
{
  "jsonrpc": "2.0",
  "id": 11,
  "method": "tools/call",
  "params": {
    "name": "delete",
    "arguments": {
      "className": "User",
      "jsonObjects": [
        {"id": 100}
      ],
      "deep": false
    }
  }
}
```

## Error Responses

If a tool call fails, ORMCP Server returns an error response:

```json
{
  "jsonrpc": "2.0",
  "id": 12,
  "error": {
    "code": -32000,
    "message": "Tool execution failed",
    "data": {
      "details": "Class 'InvalidClass' not found in object model"
    }
  }
}
```

## Request ID Guidelines

- Each request must have a unique `id` field (integer or string)
- Use sequential integers (1, 2, 3...) for simplicity
- Notifications (like `notifications/initialized`) don't include an `id`
- Responses will include the same `id` as the request

## Testing with Command Line

You can test these messages manually using the ORMCP Server in STDIO mode:

```bash
# Start ORMCP Server in STDIO mode
ormcp-server

# Or use Python module directly
python -m ormcp_server
```

Then paste the JSON messages into stdin, one per line. Each message must be on a single line (no formatting).

## Complete Session Example

Here's a complete session from connection to tool call:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"roots":{"listChanged":true},"sampling":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}

{"jsonrpc":"2.0","method":"notifications/initialized"}

{"jsonrpc":"2.0","id":2,"method":"tools/list"}

{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"getObjectModelSummary","arguments":{}}}

{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"query","arguments":{"className":"User","filter":"","maxObjects":5,"deep":false}}}
```

## See Also

- [MCP Tools API Reference](../reference/ormcp_tools_reference.md) - Detailed tool documentation
- [Interacting with ORMCP Server in STDIO Mode](Interacting_With_ORMCP_Server_In_STDIO_Mode.md) - High-level guide
- [Using the ORMCP Client Example](../client/using_ormcp_client_example.md) - Python client examples
- [Official MCP Specification](https://modelcontextprotocol.io/) - Complete protocol documentation

## Troubleshooting

**Connection issues:**
- Ensure each JSON message is on a single line (no line breaks within the JSON)
- Verify the `initialize` request includes the correct protocol version
- Check that you send the `initialized` notification after receiving the initialize response

**Tool call failures:**
- Verify the tool name is spelled correctly (case-sensitive)
- Ensure all required arguments are provided
- Check that class names match your Gilhari object model
- Review the error response for specific failure details

**Response parsing:**
- Responses are also single-line JSON messages
- Each response includes the same `id` as the request
- Look for the `result` field for successful calls or `error` field for failures
