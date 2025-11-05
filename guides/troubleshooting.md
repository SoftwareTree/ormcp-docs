Copyright (c) 2025, Software Tree

# ORMCP Server Troubleshooting Guide

Solutions to common issues and problems.

---

## Table of Contents

- [Installation Issues](#installation-issues)
- [Connection Problems](#connection-problems)
- [Configuration Issues](#configuration-issues)
- [Runtime Errors](#runtime-errors)
- [Performance Problems](#performance-problems)
- [Platform-Specific Issues](#platform-specific-issues)
- [Debug Mode](#debug-mode)
- [Getting Help](#getting-help)

---

## Installation Issues

### Empty Executable File (0 bytes)

**Problem:** The `ormcp-server.exe` file is 0 bytes and won't run.

**Cause:** Antivirus interference or file system issues during installation.

**Solution:**
```bash
# Uninstall
pip uninstall ormcp-server

# Reinstall
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ ormcp-server

# Verify
pip show ormcp-server
ormcp-server --help
```

---

### Command Not Found

**Problem:** `ormcp-server: command not found` or `'ormcp-server' is not recognized`

**Solutions:**

**1. Find Installation Location:**
```bash
# Windows (PowerShell)
(Get-Command ormcp-server -ErrorAction SilentlyContinue).Source

# Windows (Command Prompt)
where ormcp-server

# Linux/Mac
which ormcp-server

# Any platform
pip show -f ormcp-server | grep ormcp-server
```

**2. Add to PATH:**

**Windows:**
```powershell
# PowerShell (as Administrator, then restart terminal)
setx PATH "$env:PATH;$env:APPDATA\Python\Python313\Scripts"
```

**Linux/Mac:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"

# Reload
source ~/.bashrc  # or source ~/.zshrc
```

**3. Use Full Path:**
```bash
# Windows
%APPDATA%\Python\Python313\Scripts\ormcp-server.exe

# Linux/Mac
~/.local/bin/ormcp-server
```

**4. Use Python Module:**
```bash
python -m ormcp_server
```

---

### 401 Unauthorized Error (Gemfury)

**Problem:** `401 Unauthorized` when installing from Gemfury

**Solutions:**

1. **Verify Token:**
   - Check you copied the complete token
   - Ensure no extra spaces or characters
   - Try pasting in a text editor first

2. **Check Token Expiration:**
   - Request new token if expired
   - Contact ormcp_support@softwaretree.com

3. **Use Direct URL:**
   ```bash
   pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ ormcp-server
   ```

4. **Check pip Configuration:**
   ```bash
   # Linux/Mac
   cat ~/.pip/pip.conf
   
   # Windows
   type %APPDATA%\pip\pip.ini
   ```

---

### Missing Dependencies

**Problem:** `ModuleNotFoundError: No module named 'requests'` or similar

**Solution:**
```bash
# Reinstall with force
pip install --force-reinstall --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ ormcp-server

# Or install missing dependency
pip install requests

# Verify dependencies
pip show ormcp-server
# Should show: fastmcp, httpx, mcp, pydantic, uvicorn, requests
```

---

### SSL Certificate Error

**Problem:** SSL verification failed when connecting to Gemfury

**Solutions:**

**1. Update Certificates:**
```bash
pip install --upgrade certifi
```

**2. Temporary Bypass (not recommended for production):**
```bash
pip install --trusted-host pypi.fury.io --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ ormcp-server
```

---

## Connection Problems

### Gilhari Connection Refused

**Problem:** ORMCP can't connect to Gilhari microservice

**Diagnosis:**
```bash
# Test Gilhari directly
curl http://localhost:80/gilhari/v1/health/check

# Expected: 200 OK
```

**Solutions:**

**1. Verify Gilhari is Running:**
```bash
docker ps | grep gilhari

# If not running, start it:
docker run -p 80:8081 gilhari_example1:1.0
```

**2. Check Port:**
```bash
# Verify port 80 is accessible
# Windows
netstat -an | findstr :80

# Linux/Mac
lsof -i :80
```

**3. Verify GILHARI_BASE_URL:**
```bash
# Linux/Mac
echo $GILHARI_BASE_URL

# Windows (Command Prompt)
echo %GILHARI_BASE_URL%

# Windows (PowerShell)
echo $env:GILHARI_BASE_URL

# Should be: http://localhost:80/gilhari/v1/
```

**4. Try Different Port:**
```bash
# Run Gilhari on different port
docker run -p 8888:8081 gilhari_example1:1.0

# Update environment variable
export GILHARI_BASE_URL="http://localhost:8888/gilhari/v1/"
```

**5. Check Docker Network:**
```bash
# List Docker networks
docker network ls

# Inspect network
docker network inspect bridge
```

---

### Database Connection Errors

**Problem:** Gilhari can't connect to database

**Check Gilhari Logs:**
```bash
# Get container ID
docker ps

# View logs
docker logs <container-id>

# Follow logs in real-time
docker logs -f <container-id>
```

**Common Issues:**

**1. Wrong Database URL:**
```dockerfile
# Check Dockerfile environment variables
ENV DB_URL=jdbc:postgresql://correct-host:5432/mydb
ENV DB_USER=correct_user
ENV DB_PASSWORD=correct_password
```

**2. Database Not Accessible:**
```bash
# Test database connection
# PostgreSQL
psql -h localhost -U myuser -d mydb

# MySQL
mysql -h localhost -u myuser -p mydb
```

**3. Missing JDBC Driver:**
```bash
# Ensure JDBC driver is in Docker image
docker exec <container-id> ls /app/drivers/
```

**4. Firewall Blocking:**
- Check firewall allows database port
- Verify database allows connections from Docker container IP

---

### MCP Client Connection Issues

**Problem:** Claude Desktop (or other MCP client) can't connect to ORMCP

**Solutions:**

**1. Restart Client:**
- Restart Claude Desktop after changing configuration
- Clear cache if available

**2. Check Configuration File:**

**Claude Desktop Config Locations:**
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**Validate JSON Syntax:**
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

**Common JSON Errors:**
- Trailing comma after last item
- Missing quotes around strings
- Backslash not escaped in Windows paths

**3. Verify Command Path:**
```bash
# Find ormcp-server location
# Windows
where ormcp-server

# Linux/Mac
which ormcp-server

# Use full path in config:
"command": "C:\\Users\\YourUser\\AppData\\Roaming\\Python\\Python313\\Scripts\\ormcp-server.exe"
```

**4. Check Logs:**

**Claude Desktop Logs:**
- **macOS:** `~/Library/Logs/Claude/`
- **Windows:** `%APPDATA%\Claude\logs\`

**Look for:**
- Server startup errors
- Connection failures
- Environment variable issues

---

## Configuration Issues

### Environment Variables Not Set

**Problem:** ORMCP starts but can't find Gilhari

**Verify Variables:**
```bash
# Linux/Mac
env | grep GILHARI

# Windows (Command Prompt)
set | findstr GILHARI

# Windows (PowerShell)
Get-ChildItem Env: | Where-Object {$_.Name -like "*GILHARI*"}
```

**Set Variables:**

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

**For Claude Desktop:**

Add to config file (variables set per-server):
```json
{
  "mcpServers": {
    "my-ormcp-server": {
      "command": "ormcp-server",
      "env": {
        "GILHARI_BASE_URL": "http://localhost:80/gilhari/v1/",
        "MCP_SERVER_NAME": "MyORMCPServer"
      }
    }
  }
}
```

---

### Wrong Port Configuration

**Problem:** ORMCP connects to wrong port

**Check Port Mapping:**
```bash
# See where Gilhari is listening
docker ps

# Should show: 0.0.0.0:80->8081/tcp

# If different port:
docker run -p 8888:8081 gilhari_example1:1.0

# Update environment variable
export GILHARI_BASE_URL="http://localhost:8888/gilhari/v1/"
```

---

## Runtime Errors

### Tool Execution Failed

**Problem:** MCP tool calls return errors

**Common Causes:**

**1. Class Not Found:**

**Error:** `Class 'User' not found in object model`

**Solution:**
```bash
# Check object model
curl http://localhost:80/gilhari/v1/getObjectModelSummary/now

# Verify class name matches ORM specification
# Class names are case-sensitive
```

**2. Invalid Filter Syntax:**

**Error:** `Invalid filter expression`

**Solution:**
- Use SQL-like WHERE clause syntax
- Check for proper quote escaping
- Valid: `state='CA' AND age >= 30`
- Invalid: `state=CA AND age >= 30` (missing quotes)

**3. Primary Key Violation:**

**Error:** `Primary key constraint violation`

**Solution:**
- Use `update` instead of `insert` for existing records
- Check for duplicate IDs
- Verify primary key values

**4. Missing Attribute:**

**Error:** `Attribute 'xyz' not found`

**Solution:**
- Check ORM specification for attribute names
- Attribute names are case-sensitive
- Verify PERSISTENT declaration in JDX file

---

### Timeout Errors

**Problem:** Queries timeout

**Solutions:**

**1. Increase Timeout:**
```bash
# Set longer timeout (seconds)
export GILHARI_TIMEOUT=60

# Or in Claude Desktop config:
"env": {
  "GILHARI_TIMEOUT": "60"
}
```

**2. Optimize Query:**
- Add more specific filters
- Use `maxObjects` to limit results
- Use shallow queries (`deep=false`) when possible
- Use projections to retrieve only needed attributes

**3. Check Database Performance:**
- Add indexes to frequently queried columns
- Analyze slow query logs
- Check for table locks

**4. Review Gilhari Configuration:**
- Increase connection pool size
- Check database connection latency

---

### Memory Errors

**Problem:** Out of memory errors

**Solutions:**

**1. Limit Result Size:**
```json
{
  "name": "query",
  "arguments": {
    "maxObjects": 100,  // Don't retrieve all records
    "deep": false       // Don't include relationships
  }
}
```

**2. Use Pagination:**
- Retrieve data in chunks
- Process and discard before fetching next chunk

**3. Increase Docker Memory:**
```bash
# Run with more memory
docker run -m 2g -p 80:8081 gilhari_example1:1.0
```

---

## Performance Problems

### Slow Queries

**Diagnosis:**

**1. Enable Debug Logging:**
```bash
export LOG_LEVEL=DEBUG
ormcp-server
```

**2. Check SQL Statements:**

In Gilhari, set `DEBUG_LEVEL=0` (most verbose) in Dockerfile:
```dockerfile
ENV DEBUG_LEVEL=0
```

Rebuild and check logs for generated SQL.

**Solutions:**

**1. Add Database Indexes:**
```sql
-- For frequently filtered columns
CREATE INDEX idx_users_state ON users(state);
CREATE INDEX idx_users_age ON users(age);
CREATE INDEX idx_orders_date ON orders(order_date);
```

**2. Use Projections:**
```json
{
  "operationDetails": "[{\"opType\":\"projections\",\"projectionsDetails\":[{\"type\":\"User\",\"attribs\":[\"name\",\"email\"]}]}]"
}
```

**3. Optimize Relationships:**
- Use shallow queries when relationships aren't needed
- Apply filters to referenced objects
- Consider denormalizing frequently accessed data

---

### High Token Usage

**Problem:** AI responses consume too many tokens

**Solutions:**

**1. Use Shallow Queries:**
```json
{
  "deep": false  // Don't retrieve related objects
}
```

**2. Use Projections:**
- Only retrieve needed attributes
- Reduces response size

**3. Apply Filters:**
- Filter at database level, not in AI
- Reduces data transmission

**4. Limit Results:**
```json
{
  "maxObjects": 10  // Don't return all records
}
```

---

## Platform-Specific Issues

### Windows: Python Not Found

**Problem:** `'python' is not recognized`

**Solutions:**

**1. Verify Installation:**
- Open "Add or Remove Programs"
- Check if Python 3.12+ is installed

**2. Add to PATH:**
1. Search "Environment Variables" in Start Menu
2. Edit "PATH" variable
3. Add Python directories:
   - `C:\Users\<YourUser>\AppData\Local\Programs\Python\Python313\`
   - `C:\Users\<YourUser>\AppData\Local\Programs\Python\Python313\Scripts\`

**3. Use py Launcher:**
```cmd
py -3.12 -m ormcp_server
```

---

### Linux: Permission Denied

**Problem:** Permission denied when running ormcp-server

**Solution:**
```bash
# Make executable
chmod +x ~/.local/bin/ormcp-server

# Or use Python module
python -m ormcp_server
```

---

### macOS: Gatekeeper Blocking

**Problem:** macOS blocks execution due to unidentified developer

**Solution:**
1. Open System Preferences → Security & Privacy
2. Click "Allow Anyway" for ormcp-server
3. Or run: `xattr -d com.apple.quarantine ~/.local/bin/ormcp-server`

---

## Debug Mode

Enable detailed logging for troubleshooting:

### ORMCP Debug Mode

```bash
# Set debug level
export LOG_LEVEL=DEBUG

# Start server
ormcp-server

# You'll see:
# - Detailed request/response logs
# - Stack traces for errors
# - Connection attempt information
# - Environment variable values
```

### Gilhari Debug Mode

In your Dockerfile:
```dockerfile
# Most verbose (0 = maximum detail)
ENV DEBUG_LEVEL=0

# Moderate (3 = SQL statements)
ENV DEBUG_LEVEL=3

# Minimal (5 = errors only)
ENV DEBUG_LEVEL=5
```

Rebuild and run:
```bash
docker build -t my-gilhari:debug .
docker run -p 80:8081 my-gilhari:debug
```

View logs:
```bash
docker logs -f <container-id>
```

### MCP Protocol Debug

For MCP client debugging, see:
- [STDIO Mode Debug Guide](../docs/Interacting_With_ORMCP_Server_In_STDIO_Mode.md)
- [HTTP Mode Debug Guide](../docs/Interacting_With_ORMCP_Server_In_HTTP_Mode.md)

---

## Getting Help

### Before Asking for Help

Gather this information:

1. **Version Information:**
   ```bash
   pip show ormcp-server
   docker --version
   python --version
   ```

2. **Error Messages:**
   - Complete error text
   - Stack traces
   - Log files

3. **Configuration:**
   - Environment variables (sanitize sensitive data)
   - MCP client configuration
   - Gilhari Dockerfile

4. **Steps to Reproduce:**
   - Exact commands run
   - Expected vs actual behavior

### Support Channels

**GitHub Issues (Recommended):**
- [Report a Bug](https://github.com/softwaretree/ormcp-docs/issues/new?template=bug_report.md)
- [Request a Feature](https://github.com/softwaretree/ormcp-docs/issues/new?template=feature_request.md)
- [Search Existing Issues](https://github.com/softwaretree/ormcp-docs/issues)

**Email Support:**
- ormcp_support@softwaretree.com
- Include all information from "Before Asking for Help"

**Documentation:**
- [Installation Guide](installation.md)
- [Quick Start Guide](quickstart.md)
- [Gilhari Setup Guide](gilhari_setup.md)
- [MCP Tools Reference](../reference/ormcp_tools_reference.md)

---

## Common Error Messages

### "Gilhari service not responding"

**Causes:**
- Gilhari not running
- Wrong URL in GILHARI_BASE_URL
- Network/firewall issues

**Fix:** See [Gilhari Connection Refused](#gilhari-connection-refused)

---

### "Object model not found"

**Causes:**
- JDX file not loaded
- Class name mismatch
- ORM specification error

**Fix:** Check `getObjectModelSummary` and verify class names

---

### "Invalid JSON in request"

**Causes:**
- Malformed JSON syntax
- Wrong data types
- Missing required fields

**Fix:** Validate JSON syntax, check MCP Tools Reference for parameters

---

### "Connection pool exhausted"

**Causes:**
- Too many concurrent queries
- Database connections not released
- Pool size too small

**Fix:** Increase pool size in Gilhari configuration

---

## Related Documentation

- [Back to Main README](../README.md)
- [Installation Guide](installation.md)
- [Quick Start Guide](quickstart.md)
- [Gilhari Setup Guide](gilhari_setup.md)
- [MCP Tools Reference](../reference/ormcp_tools_reference.md)