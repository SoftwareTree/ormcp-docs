#!/usr/bin/env python3
"""
MCP Client - Connect to MCP servers via stdio or HTTP
# Author: Damodar Periwal

python ormcp_client_example.py --mode http --url http://127.0.0.1:8080 --demo
"""

import json
import psutil
import subprocess
import requests
import argparse
import sys
from typing import Dict, Any, Optional, List
import time
import threading


class MCPClient:
    def __init__(self):
        self.process = None
        self.base_url = None
        self.connection_type = None
        self.request_id = 1
        self.initialized = False
        self.session_id = None  # Add session ID for HTTP mode

    def connect_stdio(self, server_command=None, server_pid=0):
        """Connect to MCP server via stdio and ensure it stays alive"""
        self.connection_type = "stdio"
        try:
            if server_command:
                print(f"🔌 Starting MCP server with command: {' '.join(server_command)}", flush=True)

                # Start the server process
                self.process = subprocess.Popen(
                    server_command,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,  # Line-buffered
                    close_fds=True  # Close file descriptors
                )

                print("🟢 Server started and running in the background...", flush=True)

                # Function to read stderr in a separate thread
                def read_stderr():
                    if self.process is None or self.process.stderr is None:
                        print("❌ Server STDERR: stderr is not available", flush=True)
                        return False
                    while True:
                        try:
                            stderr_output = self.process.stderr.readline()
                            if stderr_output == "" and self.process.poll() is not None:
                                break
                            if stderr_output:
                                print(f"🛑 Server STDERR: {stderr_output.strip()}", flush=True)
                        except ValueError:
                            # Handle closed file
                            break

                # Start stderr reader in a separate thread
                stderr_thread = threading.Thread(target=read_stderr, daemon=True)
                stderr_thread.start()

                # Wait for the process to initialize properly before proceeding
                time.sleep(2)

                # Check if stdin/stdout are open (dynamic check)
                if self.process.stdin is None or self.process.stdout is None:
                    print("❌ Error: Server stdin or stdout are not available.", flush=True)
                    return False

                # Send proper initialization message
                init_message = {
                    "jsonrpc": "2.0",
                    "id": self._next_id(),
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "roots": {"listChanged": True},
                            "sampling": {}
                        },
                        "clientInfo": {
                            "name": "python-mcp-client",
                            "version": "1.0.0"
                        }
                    }
                }

                response = self._send_stdio_message(init_message)
                if response and not response.get("error"):
                    print(f"✅ Server initialized successfully", flush=True)
                    self.initialized = True
                    
                    # Send initialized notification
                    initialized_notification = {
                        "jsonrpc": "2.0",
                        "method": "notifications/initialized"
                    }
                    self._send_stdio_message(initialized_notification)
                    
                    return True
                else:
                    print(f"❌ Server initialization failed: {response}", flush=True)
                    return False

            else:
                print("❌ No server process connected.", flush=True)
                return False

        except Exception as e:
            print(f"❌ Error in stdio communication: {e}", flush=True)
            return False
    
    def connect_to_running_server(self, pid):
        """Connect to the already running MCP server by its PID."""
        self.connection_type = "stdio"
        try:
            # Find the process by PID
            process = psutil.Process(pid)

            # Get the process's stdin and stdout streams
            self.process = subprocess.Popen(process.cmdline(),
                                            stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            text=True)
            if not self.process:
                print("❌ No process available")
                return None
            
            # Send proper initialization message
            init_message = {
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "roots": {"listChanged": True},
                        "sampling": {}
                    },
                    "clientInfo": {
                        "name": "python-mcp-client",
                        "version": "1.0.0"
                    }
                }
            }

            response = self._send_stdio_message(init_message)
            if response and not response.get("error"):
                print(f"✅ Server initialized successfully", flush=True)
                self.initialized = True
                
                # Send initialized notification
                initialized_notification = {
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized"
                }
                
            self.initialized = True
            return True

        except Exception as e:
            print(f"❌ Error in connecting to the running server: {e}")
            return False

    def stop_server(self):
        """Stop the running server gracefully"""
        if self.process:
            print("🔴 Stopping the server...")
            self.process.terminate()  # Gracefully stop the server
            self.process.wait()  # Wait for the process to terminate
            print("Server stopped.")
        else:
            print("❌ No server to stop.")

    def connect_http(self, base_url: str) -> bool:
        """Connect to MCP server via HTTP using FastMCP protocol"""
        try:
            # Ensure URL ends with /mcp/
            if not base_url.endswith('/mcp/'):
                if base_url.endswith('/mcp'):
                    base_url = base_url + '/'
                elif base_url.endswith('/'):
                    base_url = base_url + 'mcp/'
                else:
                    base_url = base_url + '/mcp/'
            
            self.base_url = base_url
            self.connection_type = "http"

            # Test connection with initialize
            init_response = self._send_http_message({
                "jsonrpc": "2.0",
                "id": self._next_id(),
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "roots": {"listChanged": True},
                        "sampling": {}
                    },
                    "clientInfo": {
                        "name": "python-mcp-client",
                        "version": "1.0.0"
                    }
                }
            })

            if init_response and not init_response.get("error"):
                print(f"✅ Successfully connected to {base_url}")
                self.initialized = True
                
                # Send initialized notification (required for FastMCP)
                self._send_http_message({
                    "jsonrpc": "2.0",
                    "method": "notifications/initialized"
                })
                
                return True
            else:
                print(f"❌ Failed to connect to {base_url}: {init_response}")
                return False

        except Exception as e:
            print(f"❌ Failed to connect via HTTP: {e}")
            return False

    def _next_id(self) -> int:
        """Get next request ID"""
        current_id = self.request_id
        self.request_id += 1
        return current_id

    def _parse_sse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Server-Sent Events response format for FastMCP."""
        lines = response_text.strip().split('\n')
        data_line = None
        
        for line in lines:
            if line.startswith('data: '):
                data_line = line[6:]  # Remove 'data: ' prefix
                break
        
        if data_line:
            try:
                return json.loads(data_line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON data: {data_line}") from e
        else:
            # If no SSE format, try parsing as direct JSON
            try:
                return json.loads(response_text.strip())
            except json.JSONDecodeError:
                raise ValueError(f"No valid data found in response: {response_text}")

    def _send_stdio_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send message via stdio and get response"""
        if not self.process:
            print("❌ No process available")
            return None

        try:
            # Check if process is still running
            if self.process.poll() is not None:
                print("❌ Server process is no longer running")
                return None

            json_message = json.dumps(message)
            print(f"📤 Sending: {json_message}")
            
            if self.process.stdin.closed:
                print("❌ stdin is closed!")
                return None
            
            self.process.stdin.write(json_message + '\n')
            self.process.stdin.flush()

            # For notifications (no id field), don't expect a response
            if "id" not in message:
                print("📤 Notification sent (no response expected)")
                return {"success": True}

            stdout_output = self.process.stdout.readline()
            if stdout_output:
                if stdout_output.strip():
                    print(f"📥 Received: {stdout_output.strip()}")
                    return json.loads(stdout_output.strip())
            else:
                print("❌ No output received or stdout is closed!")

            return None

        except Exception as e:
            print(f"❌ Error in stdio communication: {e}")
            return None

    def _send_http_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send message via HTTP using FastMCP streaming protocol"""
        if not self.base_url:
            print("❌ Base URL not provided for HTTP")
            return None

        try:
            print(f"📤 Sending HTTP: {json.dumps(message, indent=2)}")
            
            # Setup headers for FastMCP streaming protocol
            headers = {
                'Accept': 'application/json, text/event-stream',
                'Content-Type': 'application/json'
            }
            
            # Add session ID if we have one
            if self.session_id:
                headers['mcp-session-id'] = self.session_id
            
            response = requests.post(
                self.base_url,
                json=message,
                headers=headers,
                timeout=30
            )
            
            # Extract session ID from response headers if present
            if 'mcp-session-id' in response.headers:
                self.session_id = response.headers['mcp-session-id']
                print(f"📋 Session ID: {self.session_id}")
            
            # Handle different response scenarios
            if response.status_code == 200:
                if response.text.strip():
                    # Parse SSE format response
                    result = self._parse_sse_response(response.text)
                    print(f"📥 Received HTTP: {json.dumps(result, indent=2)}")
                    return result
                else:
                    # Empty response (likely a notification)
                    print("📥 Received empty response (notification)")
                    return {"success": True}
            else:
                # Handle error responses
                try:
                    if response.text.startswith('event:') or response.text.startswith('data:'):
                        error_data = self._parse_sse_response(response.text)
                    else:
                        error_data = response.json()
                    print(f"❌ HTTP Error: {error_data}")
                    return error_data
                except:
                    response.raise_for_status()

        except Exception as e:
            print(f"❌ Error in HTTP communication: {e}")
            return None

    def send_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send message using the appropriate transport"""
        if not self.initialized:
            print("❌ Client not initialized. Call connect_stdio or connect_http first.")
            return None
            
        if self.connection_type == "stdio":
            return self._send_stdio_message(message)
        elif self.connection_type == "http":
            return self._send_http_message(message)
        else:
            print("❌ No connection established")
            return None

    def capture_server_logs(self):
        """Capture server logs from the process - removed because it blocks"""
        # This method was causing issues by calling communicate() which blocks
        # and closes the pipes. We're already capturing stderr in the thread.
        pass

    def list_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools"""
        print("\n🔧 Listing available tools...")

        response = self.send_message({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/list"
        })

        if response and "result" in response:
            tools = response["result"].get("tools", [])
            print(f"📋 Found {len(tools)} tool(s):")
            for i, tool in enumerate(tools, 1):
                print(f"  {i}. {tool.get('name', 'Unknown')} - {tool.get('description', 'No description')}")
            return tools
        else:
            print("❌ Failed to get tools list")
            return []

    def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Call a specific tool"""
        print(f"\n🛠️  Calling tool: {tool_name}")
        if arguments:
            print(f"   Arguments: {arguments}")

        response = self.send_message({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        })

        if response and "result" in response:
            print(f"✅ Tool result: {json.dumps(response['result'], indent=2)}")
            return response["result"]
        else:
            print(f"❌ Tool call failed: {response}")
            return None

    def list_resources(self) -> List[Dict[str, Any]]:
        """Get list of available resources"""
        print("\n📚 Listing available resources...")

        response = self.send_message({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "resources/list"
        })

        if response and "result" in response:
            resources = response["result"].get("resources", [])
            print(f"📋 Found {len(resources)} resource(s):")
            for i, resource in enumerate(resources, 1):
                print(f"  {i}. {resource.get('uri', 'Unknown')} - {resource.get('description', 'No description')}")
            return resources
        else:
            print("❌ Failed to get resources list")
            return []
    
    def read_resource(self, uri: str, arguments: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]: 
        """Read a specific resource by URI"""
        
        response = self.send_message({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "resources/read",
            "params": {
                "uri": uri
            }
        })
        
        if response and "result" in response:
            print(f"✅ Resource result: {json.dumps(response['result'], indent=2)}")
            return response["result"]
        else:
            print(f"❌ Resource call failed: {response}")
            return None      

    def demo_session(self):
        """Run a demonstration session"""
        print("\n🎯 Starting demo session...")

        # List tools
        tools = self.list_tools()

        # List resources
        resources = self.list_resources()

        if tools:
            print(f"\n🎮 Trying to call some tools...")

            # Try to call first few tools with reasonable defaults
            for tool in tools[:3]:  # Limit to first 3 tools
                tool_name = tool.get("name")
                if not tool_name:
                    continue

                # Try to determine reasonable arguments based on tool schema
                arguments = self._get_demo_arguments(tool)

                print(f"\n--- Calling {tool_name} ---")
                self.call_tool(tool_name, arguments)

                # Small delay between calls
                time.sleep(1)
        else:
            print("❌ No tools available for demo")

    def _get_demo_arguments(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """Generate demo arguments for a tool based on its schema"""
        arguments = {}
        input_schema = tool.get("inputSchema", {})
        properties = input_schema.get("properties", {})

        # Generate reasonable demo values
        for prop_name, prop_info in properties.items():
            prop_type = prop_info.get("type", "string")
            arguments[prop_name] = self._generate_demo_value(prop_name, prop_type)

        return arguments

    def _generate_demo_value(self, prop_name: str, prop_type: str) -> Any:
        """Generate demo value based on property type"""
        if prop_type == "integer":
            return 42 if "num" in prop_name else 10
        elif prop_type == "string":
            if "name" in prop_name.lower():
                return "demo_object"
            elif "filter" in prop_name.lower():
                return ""
            else:
                return "demo_value"
        elif prop_type == "boolean":
            return True
        elif prop_type == "array":
            return []
        elif prop_type == "object":
            return {}
        return None

    def close(self):
        """Close the connection"""
        if self.process:
            print("🔌 Closing stdio connection...")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            self.process = None

        self.connection_type = None
        self.base_url = None
        self.session_id = None
        self.initialized = False


def main():
    parser = argparse.ArgumentParser(description="MCP Client - Connect to MCP servers")

    # Connection type
    parser.add_argument(
        "--mode",
        choices=["stdio", "http"],
        default="stdio",
        help="Connection mode"
    )

    # Stdio options
    parser.add_argument(
        "--server_cmd",
        default="C:\\Users\\dperi\\.local\\bin\\uv.exe run --with fastmcp fastmcp run c:\\Users\\Damodar\\VSCode\\ormcp_server_project\\src\\ormcp_server.py",
        help="Command to start MCP server for stdio mode"
    )

    # MCP server pid options
    parser.add_argument(
        "--server_pid",
        type=int,
        help="Command to connect to an existing MCP server with the given pid in stdio mode"
    )

    # HTTP options
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8080",
        help="URL of HTTP MCP server"
    )

    # Action options
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demo session (list tools and call some)"
    )

    args = parser.parse_args()

    client = MCPClient()

    try:
        # Connect based on mode
        if args.mode == "stdio":
            if (args.server_pid):
                if not client.connect_to_running_server(args.server_pid):
                    sys.exit(1)
            elif (args.server_cmd):
                server_command = args.server_cmd.split()
                if not client.connect_stdio(server_command):
                    sys.exit(1)
            else: 
                print("\n🎮 No MCP Server command or PID specified; exiting.")
                sys.exit(1)
            
        elif args.mode == "http":
            if not client.connect_http(args.url):
                sys.exit(1)
                

        # Run demo or interactive session
        if args.demo:
            client.demo_session()
        else:
            # Interactive session
            print("\n🎮 Interactive MCP Client")
            print("Commands: tools, resources, call <tool_name> [args_json], quit")

            while True:
                try:
                    command = input("\n> ").strip()

                    if command == "quit":
                        break
                    elif command == "tools":
                        client.list_tools()
                    elif command == "resources":
                        client.list_resources()
                    elif command.startswith("call "):
                        parts = command.split(" ", 2)
                        tool_name = parts[1]
                        args_json = parts[2] if len(parts) > 2 else "{}"
                        try:
                            arguments = json.loads(args_json)
                            client.call_tool(tool_name, arguments)
                        except json.JSONDecodeError as e:
                            print(f"❌ Invalid JSON arguments: {e}")
                    elif command.startswith("read "):
                        parts = command.split(" ", 2)
                        resource_name = parts[1]
                        args_json = parts[2] if len(parts) > 2 else "{}"
                        try:
                            arguments = json.loads(args_json)
                            client.read_resource(resource_name, arguments)
                        except json.JSONDecodeError as e:
                            print(f"❌ Invalid JSON arguments: {e}")
                    else:
                        print("Unknown command. Use: tools, resources, call <tool_name> [args_json], quit")

                except KeyboardInterrupt:
                    break
                except EOFError:
                    break

    finally:
        client.close()
        print("👋 Goodbye!")


if __name__ == "__main__":
    main()