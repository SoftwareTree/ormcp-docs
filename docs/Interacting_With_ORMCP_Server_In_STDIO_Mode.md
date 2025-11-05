Copyright (c) 2025, Software Tree

# Interacting with ORMCP Server in stdio Mode - User Guide

This guide explains how to interact with an ORMCP (Model Context Protocol) server running in stdio (standard input/output) mode. Unlike HTTP mode, stdio mode uses direct process communication through stdin/stdout.

## Prerequisites

When your ORMCP server starts in stdio mode, it typically:
- Reads JSON-RPC messages from stdin (standard input)
- Writes responses to stdout (standard output) 
- May write logs to stderr (standard error)
- Does not bind to any network port

## Understanding stdio Mode

In stdio mode:
- **No HTTP server** - no URLs or ports
- **Direct process communication** - messages sent via stdin/stdout
- **JSON-RPC over pipes** - each message is a complete JSON-RPC object
- **Newline-delimited** - each message typically ends with a newline
- **Bidirectional** - server can send notifications back to client

## Method 1: Command Line Interaction (Manual)

### Step 1: Start the ORMCP Server
```bash
# Start your ORMCP server in stdio mode (default mode)
python src\ormcp_server.py --transport stdio
```

Or if using a different command:
```bash
./ormcp_server --mode stdio
```

### Step 2: Send Messages via stdin
Once the ORMCP server is running, you can type JSON-RPC messages directly:

**Initialize the connection:**
```json
{"jsonrpc":"2.0","id":"1","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"manual-client","version":"1.0.0"}}}
```

**Send initialized notification:**
```json
{"jsonrpc":"2.0","method":"notifications/initialized"}
```

**List tools:**
```json
{"jsonrpc":"2.0","id":"2","method":"tools/list"}
```

**Call a tool:**
```json
{"jsonrpc":"2.0","id":"3","method":"tools/call","params":{"name":"add","arguments":{"a":5,"b":3}}}
```

### Important Notes for Manual Interaction:
- Press `Enter` after each JSON message
- The server will respond immediately after each message
- Use `Ctrl+C` to exit
- Watch both stdout (responses) and stderr (logs)

## Method 2: Using echo and Pipes (Linux/Mac)

### Basic Interaction Script
```bash
#!/bin/bash

# Start the server in background
python src\ormcp_server.py --transport stdio &
SERVER_PID=$!

# Function to send message
send_message() {
    echo "$1" 
}

# Initialize
send_message '{"jsonrpc":"2.0","id":"1","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"pipe-client","version":"1.0.0"}}}' | python your_mcp_server.py --transport stdio

# Clean up
kill $SERVER_PID
```

### Using Named Pipes (Advanced)
```bash
# Create named pipes
mkfifo server_input
mkfifo server_output

# Start server with pipes
python src\ormcp_server.py --transport stdio < server_input > server_output &
SERVER_PID=$!

# Send messages
echo '{"jsonrpc":"2.0","id":"1","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"pipe-client","version":"1.0.0"}}}' > server_input

# Read responses
cat server_output &

# Cleanup
kill $SERVER_PID
rm server_input server_output
```

## Method 3: Python Client Script

Create a Python script to interact with ORMCP server:

```python
#!/usr/bin/env python3
import subprocess
import json
import threading
import queue
import sys

class MCPStdioClient:
    def __init__(self, server_command):
        self.server_process = subprocess.Popen(
            server_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )
        self.response_queue = queue.Queue()
        self.running = True
        
        # Start response reader thread
        self.reader_thread = threading.Thread(target=self._read_responses)
        self.reader_thread.daemon = True
        self.reader_thread.start()
        
        # Start error reader thread  
        self.error_thread = threading.Thread(target=self._read_errors)
        self.error_thread.daemon = True
        self.error_thread.start()

    def _read_responses(self):
        """Read responses from server stdout"""
        try:
            while self.running:
                line = self.server_process.stdout.readline()
                if not line:
                    break
                try:
                    response = json.loads(line.strip())
                    self.response_queue.put(response)
                    print(f"← Response: {json.dumps(response, indent=2)}")
                except json.JSONDecodeError:
                    print(f"← Raw: {line.strip()}")
        except Exception as e:
            print(f"Error reading responses: {e}")

    def _read_errors(self):
        """Read errors from server stderr"""
        try:
            while self.running:
                line = self.server_process.stderr.readline()
                if not line:
                    break
                print(f"⚠ Server log: {line.strip()}")
        except Exception as e:
            print(f"Error reading stderr: {e}")

    def send_message(self, message):
        """Send a message to the server"""
        try:
            json_str = json.dumps(message)
            print(f"→ Sending: {json_str}")
            self.server_process.stdin.write(json_str + "\n")
            self.server_process.stdin.flush()
        except Exception as e:
            print(f"Error sending message: {e}")

    def wait_for_response(self, timeout=5):
        """Wait for a response"""
        try:
            return self.response_queue.get(timeout=timeout)
        except queue.Empty:
            print("⏰ Timeout waiting for response")
            return None

    def close(self):
        """Close the client"""
        self.running = False
        try:
            self.server_process.stdin.close()
            self.server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.server_process.kill()

def main():
    # Replace with your server command
    server_cmd = ["python", "src\ormcp_server.py", "--transport stdio"]
    
    client = MCPStdioClient(server_cmd)
    
    try:
        # Initialize
        print("\n=== Initializing ===")
        client.send_message({
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "python-client", "version": "1.0.0"}
            }
        })
        init_response = client.wait_for_response()
        
        # Send initialized notification
        print("\n=== Sending initialized notification ===")
        client.send_message({
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        })
        
        # List tools
        print("\n=== Listing tools ===")
        client.send_message({
            "jsonrpc": "2.0",
            "id": "2",
            "method": "tools/list"
        })
        tools_response = client.wait_for_response()
        
        # Call add tool
        print("\n=== Calling add tool ===")
        client.send_message({
            "jsonrpc": "2.0",
            "id": "3",
            "method": "tools/call",
            "params": {
                "name": "add",
                "arguments": {"a": 10, "b": 5}
            }
        })
        add_response = client.wait_for_response()
        
        # Get object model
        print("\n=== Getting object model ===")
        client.send_message({
            "jsonrpc": "2.0",
            "id": "4",
            "method": "tools/call",
            "params": {
                "name": "getObjectModelSummary",
                "arguments": {}
            }
        })
        model_response = client.wait_for_response()
        
        # Interactive mode
        print("\n=== Interactive mode (type 'quit' to exit) ===")
        message_id = 5
        while True:
            try:
                user_input = input("\nEnter JSON message (or 'quit'): ")
                if user_input.lower() == 'quit':
                    break
                    
                # Try to parse as JSON
                try:
                    message = json.loads(user_input)
                    if 'id' not in message:
                        message['id'] = str(message_id)
                        message_id += 1
                    client.send_message(message)
                    response = client.wait_for_response()
                except json.JSONDecodeError:
                    print("❌ Invalid JSON format")
                    
            except KeyboardInterrupt:
                break
                
    finally:
        client.close()
        print("\n👋 Client closed")

if __name__ == "__main__":
    main()
```

### Usage:
```bash
# Make the script executable
chmod +x mcp_stdio_client.py

# Run the client
./mcp_stdio_client.py
```

## Method 4: Node.js Client Script

```javascript
#!/usr/bin/env node
const { spawn } = require('child_process');
const readline = require('readline');

class MCPStdioClient {
    constructor(serverCommand, serverArgs = []) {
        this.serverProcess = spawn(serverCommand, serverArgs, {
            stdio: ['pipe', 'pipe', 'pipe']
        });
        
        this.setupEventHandlers();
        this.messageId = 1;
    }
    
    setupEventHandlers() {
        // Handle stdout (responses)
        this.serverProcess.stdout.on('data', (data) => {
            const lines = data.toString().split('\n').filter(line => line.trim());
            lines.forEach(line => {
                try {
                    const response = JSON.parse(line);
                    console.log('← Response:', JSON.stringify(response, null, 2));
                } catch (e) {
                    console.log('← Raw:', line);
                }
            });
        });
        
        // Handle stderr (logs)
        this.serverProcess.stderr.on('data', (data) => {
            console.log('⚠ Server log:', data.toString().trim());
        });
        
        // Handle process exit
        this.serverProcess.on('close', (code) => {
            console.log(`Server exited with code ${code}`);
        });
    }
    
    sendMessage(message) {
        const jsonStr = JSON.stringify(message);
        console.log('→ Sending:', jsonStr);
        this.serverProcess.stdin.write(jsonStr + '\n');
    }
    
    async initialize() {
        this.sendMessage({
            jsonrpc: "2.0",
            id: this.messageId++,
            method: "initialize",
            params: {
                protocolVersion: "2024-11-05",
                capabilities: {},
                clientInfo: {name: "node-client", version: "1.0.0"}
            }
        });
        
        // Send initialized notification
        await this.sleep(1000);
        this.sendMessage({
            jsonrpc: "2.0",
            method: "notifications/initialized"
        });
    }
    
    async listTools() {
        this.sendMessage({
            jsonrpc: "2.0",
            id: this.messageId++,
            method: "tools/list"
        });
    }
    
    async callTool(name, args) {
        this.sendMessage({
            jsonrpc: "2.0",
            id: this.messageId++,
            method: "tools/call",
            params: {name, arguments: args}
        });
    }
    
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    async startInteractive() {
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        
        console.log('\n=== Interactive mode (type "quit" to exit) ===');
        
        const askQuestion = () => {
            rl.question('\nEnter JSON message (or "quit"): ', async (input) => {
                if (input.toLowerCase() === 'quit') {
                    rl.close();
                    this.close();
                    return;
                }
                
                try {
                    const message = JSON.parse(input);
                    if (!message.id && message.method !== 'notifications/initialized') {
                        message.id = this.messageId++;
                    }
                    this.sendMessage(message);
                } catch (e) {
                    console.log('❌ Invalid JSON format');
                }
                
                await this.sleep(500);
                askQuestion();
            });
        };
        
        askQuestion();
    }
    
    close() {
        this.serverProcess.kill();
    }
}

async function main() {
    // Replace with your server command
    const client = new MCPStdioClient('python', ['src\ormcp_server.py', '--transport stdio']);
    
    try {
        console.log('=== Initializing ===');
        await client.initialize();
        
        await client.sleep(2000);
        
        console.log('\n=== Listing tools ===');
        await client.listTools();
        
        await client.sleep(2000);
        
        console.log('\n=== Calling add tool ===');
        await client.callTool('add', {a: 15, b: 25});
        
        await client.sleep(2000);
        
        await client.startInteractive();
        
    } catch (error) {
        console.error('Error:', error);
        client.close();
    }
}

if (require.main === module) {
    main();
}
```

### Usage:
```bash
# Install Node.js if needed, then run:
node mcp_stdio_client.js
```

## Method 5: Using PowerShell (Windows)

```powershell
# PowerShell script for Windows
function Send-MCPMessage {
    param(
        [Parameter(Mandatory=$true)]
        [object]$Message,
        
        [Parameter(Mandatory=$true)]
        [System.Diagnostics.Process]$Process
    )
    
    $jsonString = $Message | ConvertTo-Json -Compress
    Write-Host "→ Sending: $jsonString" -ForegroundColor Green
    $Process.StandardInput.WriteLine($jsonString)
    $Process.StandardInput.Flush()
}

function Start-MCPClient {
    param([string]$ServerPath)
    
    # Start the server process
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = "python"
    $psi.Arguments = "$ServerPath --transport stdio"
    $psi.UseShellExecute = $false
    $psi.RedirectStandardInput = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.CreateNoWindow = $true
    
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $psi
    $process.Start()
    
    # Start background jobs to read output
    $outputJob = Start-Job -ScriptBlock {
        param($p)
        while (!$p.HasExited) {
            $line = $p.StandardOutput.ReadLine()
            if ($line) {
                Write-Output "← Response: $line"
            }
        }
    } -ArgumentList $process
    
    $errorJob = Start-Job -ScriptBlock {
        param($p)
        while (!$p.HasExited) {
            $line = $p.StandardError.ReadLine()
            if ($line) {
                Write-Output "⚠ Log: $line"
            }
        }
    } -ArgumentList $process
    
    try {
        # Initialize
        Write-Host "=== Initializing ===" -ForegroundColor Yellow
        Send-MCPMessage -Message @{
            jsonrpc = "2.0"
            id = "1"
            method = "initialize"
            params = @{
                protocolVersion = "2024-11-05"
                capabilities = @{}
                clientInfo = @{
                    name = "powershell-client"
                    version = "1.0.0"
                }
            }
        } -Process $process
        
        Start-Sleep -Seconds 2
        
        # Send initialized notification
        Write-Host "=== Sending initialized notification ===" -ForegroundColor Yellow
        Send-MCPMessage -Message @{
            jsonrpc = "2.0"
            method = "notifications/initialized"
        } -Process $process
        
        Start-Sleep -Seconds 1
        
        # List tools
        Write-Host "=== Listing tools ===" -ForegroundColor Yellow
        Send-MCPMessage -Message @{
            jsonrpc = "2.0"
            id = "2"
            method = "tools/list"
        } -Process $process
        
        Start-Sleep -Seconds 2
        
        # Interactive mode
        Write-Host "=== Interactive mode (type 'quit' to exit) ===" -ForegroundColor Yellow
        $messageId = 3
        
        while ($true) {
            $input = Read-Host "`nEnter JSON message (or 'quit')"
            
            if ($input -eq "quit") {
                break
            }
            
            try {
                $message = $input | ConvertFrom-Json
                if (-not $message.id -and $message.method -ne "notifications/initialized") {
                    $message | Add-Member -Name "id" -Value $messageId.ToString() -MemberType NoteProperty
                    $messageId++
                }
                Send-MCPMessage -Message $message -Process $process
                Start-Sleep -Seconds 1
            }
            catch {
                Write-Host "❌ Invalid JSON format" -ForegroundColor Red
            }
        }
    }
    finally {
        # Cleanup
        $process.Kill()
        Stop-Job $outputJob, $errorJob
        Remove-Job $outputJob, $errorJob
    }
}

# Usage
Start-MCPClient -ServerPath "ormcp_server.py"
```

## Key Differences from HTTP Mode

| Aspect | HTTP Mode | stdio Mode |
|--------|-----------|------------|
| **Connection** | TCP socket to server | Direct process pipes |
| **Transport** | HTTP with Server-Sent Events | JSON-RPC over stdin/stdout |
| **Session Management** | Session ID in headers | Process-bound session |
| **Debugging** | Network tools, browser devtools | Process monitoring, logs |
| **Scaling** | Multiple concurrent clients | One client per server process |
| **Error Handling** | HTTP status codes | JSON-RPC error responses |

## Troubleshooting stdio Mode

### Common Issues:

1. **Server doesn't respond**: Check if server is reading from stdin correctly
2. **Broken pipe errors**: Server process may have crashed - check stderr
3. **JSON parsing errors**: Ensure messages are properly formatted and newline-terminated
4. **Hanging connections**: Server may be waiting for specific initialization sequence
5. **Output mixing**: Separate stdout (responses) from stderr (logs) in your client

### Debugging Tips:
- Use `strace` (Linux) or `Process Monitor` (Windows) to monitor process I/O
- Redirect stderr to a file to separate logs from responses
- Add verbose logging to see the exact message flow
- Test with simple echo commands first

Choose the method that best fits your development workflow and technical requirements!