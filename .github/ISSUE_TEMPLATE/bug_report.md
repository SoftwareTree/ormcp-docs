---
name: Bug Report
about: Report a bug or issue with ORMCP Server
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

**A clear and concise description of what the bug is.**

## To Reproduce

Steps to reproduce the behavior:

1. Go to '...'
2. Run command '...'
3. Execute query '...'
4. See error

## Expected Behavior

**A clear and concise description of what you expected to happen.**

## Actual Behavior

**What actually happened?**

## Error Messages

```
Paste any error messages, stack traces, or log output here
```

## Environment

**ORMCP Server:**
- Version: [e.g., 0.4.3]
- Installation method: [PyPI / Gemfury]
- Transport mode: [STDIO / HTTP]

**System:**
- OS: [e.g., Windows 11, macOS 14, Ubuntu 22.04]
- Python version: [e.g., 3.12.1]
- Docker version: [e.g., 24.0.6]

**Gilhari:**
- Gilhari version: [e.g., latest]
- Database: [e.g., PostgreSQL 15, SQLite 3.42]
- Example used: [e.g., gilhari_example1]

**MCP Client:**
- Client: [e.g., Claude Desktop 0.7.1]
- Configuration: [Paste relevant config, sanitize sensitive data]

## Configuration

**Environment Variables:**
```bash
GILHARI_BASE_URL=http://localhost:80/gilhari/v1/
MCP_SERVER_NAME=MyORMCPServer
# Add other relevant variables
```

**MCP Client Config:**
```json
{
  "mcpServers": {
    "my-ormcp-server": {
      // Paste your configuration here (remove sensitive data)
    }
  }
}
```

## Logs

**ORMCP Server Logs:**
```
Paste relevant ORMCP logs here
```

**Gilhari Logs:**
```bash
# Get with: docker logs <container-id>
Paste relevant Gilhari logs here
```

**MCP Client Logs:**
```
Paste relevant client logs here (if available)
```

## Screenshots

**If applicable, add screenshots to help explain your problem.**

## Additional Context

**Add any other context about the problem here.**

- Have you tried the troubleshooting guide?
- Does this happen consistently or intermittently?
- Did this work before? When did it stop working?
- Any recent changes to your setup?

## Possible Solution

**If you have ideas about what might be causing this, share them here.**