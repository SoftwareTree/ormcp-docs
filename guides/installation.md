Copyright (c) 2025, Software Tree

# ORMCP Server Installation Guide

Complete installation instructions for ORMCP Server.

---

## System Requirements

### Software Requirements
- **Python:** 3.12 or higher
- **Docker:** Required for Gilhari microservice
- **JDBC Driver:** For your target database (included in Gilhari image)

### Operating Systems
- Linux (any distribution with Python 3.12+)
- macOS 10.14+
- Windows 10/11

### Hardware Requirements
- **Disk Space:** 
  - ~50KB for ORMCP Server wheel
  - ~100MB total with Python dependencies
  - ~1.3GB for Gilhari Docker image
- **Memory:** 
  - Minimum: 512MB
  - Recommended: 2GB+ for production

---

## Installation Methods

### Method 1: Gemfury Private PyPI (Beta)

ORMCP Server beta is distributed via Gemfury, a private PyPI repository.

#### Step 1: Request Beta Access

Visit [softwaretree.com/products/ormcp](https://www.softwaretree.com) to request beta access. You'll receive:
- Beta access token
- Evaluation period information
- Welcome email with instructions

#### Step 2: Install with Token

**Quick Installation (Recommended):**
```bash
# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install ORMCP Server from Gemfury
# Note: --extra-index-url is required because build dependencies (like hatchling) 
# are available on PyPI but not on Gemfury
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server
```

Replace `YOUR_TOKEN` with your beta access token.

**Alternative: Configure pip Permanently**

This avoids typing the token every time:

**Linux/Mac:**
Create or edit `~/.pip/pip.conf`:
```ini
[global]
index-url = https://YOUR_TOKEN@pypi.fury.io/softwaretree/
extra-index-url = https://pypi.org/simple
```

**Windows:**
Create or edit `%APPDATA%\pip\pip.ini`:
```ini
[global]
index-url = https://YOUR_TOKEN@pypi.fury.io/softwaretree/
extra-index-url = https://pypi.org/simple
```

Then install normally:
```bash
pip install ormcp-server
```

#### Step 3: Verify Installation

```bash
# Check installation
pip show ormcp-server

# Verify command works
ormcp-server --help

# Expected output:
# ORMCP Server v0.4.x
# Usage: ormcp-server [OPTIONS]
```

---

### Method 2: PyPI (Production) - Coming Soon

After beta, ORMCP Server will be available on the main PyPI repository:

```bash
# Virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install
pip install ormcp-server
```

---

## Virtual Environment Setup (Recommended)

Using a virtual environment isolates ORMCP Server and its dependencies.

### Create Virtual Environment

```bash
# Create
python -m venv .venv

# Activate
# Linux/Mac:
source .venv/bin/activate

# Windows (Command Prompt):
.venv\Scripts\activate

# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### Install ORMCP Server

```bash
# Beta (Gemfury)
# Note: --extra-index-url is required for build dependencies
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server

# Production (PyPI) - coming soon
# pip install ormcp-server
```

### Deactivate When Done

```bash
deactivate
```

---

## Platform-Specific Instructions

### Windows Setup

#### 1. Install Python 3.12+

Download from [python.org](https://www.python.org/downloads/)

**Important:** Check "Add Python to PATH" during installation.

#### 2. Add Scripts to PATH

If you didn't check "Add to PATH" during installation:

**Option 1: Quick Command (PowerShell as Administrator)**
```powershell
setx PATH "%PATH%;%APPDATA%\Python\Python313\Scripts"
```

Then **restart your terminal**.

**Option 2: Manual (Control Panel)**
1. Open "System Properties" → "Environment Variables"
2. Edit "PATH" variable
3. Add: `C:\Users\<YourUsername>\AppData\Roaming\Python\Python313\Scripts`
4. Click OK and restart terminal

#### 3. Install ORMCP Server

```bash
# Using Command Prompt or PowerShell
# Note: --extra-index-url is required for build dependencies
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server
```

#### 4. Verify

```bash
# Test command
ormcp-server --help

# If "command not found", use full path:
%APPDATA%\Python\Python313\Scripts\ormcp-server.exe

# Or use Python module:
python -m ormcp_server
```

---

### Linux Setup

#### 1. Install Python 3.12+

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
```

**Fedora:**
```bash
sudo dnf install python3.12
```

**Arch:**
```bash
sudo pacman -S python
```

#### 2. Install ORMCP Server

```bash
# With virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Note: --extra-index-url is required for build dependencies
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server
```

#### 3. Add to PATH (if needed)

If `ormcp-server` command is not found:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

---

### macOS Setup

#### 1. Install Python 3.12+

**Using Homebrew (recommended):**
```bash
brew install python@3.12
```

**Or download from:**
https://www.python.org/downloads/macos/

#### 2. Install ORMCP Server

```bash
# With virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Note: --extra-index-url is required for build dependencies
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server
```

#### 3. Add to PATH (if needed)

```bash
# Add to ~/.zshrc or ~/.bash_profile
export PATH="$HOME/.local/bin:$PATH"

# Reload shell
source ~/.zshrc  # or source ~/.bash_profile
```

---

## Troubleshooting Installation

### Issue: 401 Unauthorized Error

**Problem:** `401 Unauthorized` when installing from Gemfury

**Solutions:**
1. **Verify token** - Check you copied the complete token
2. **Check expiration** - Request new token if expired
3. **Try direct URL** - Use full index URL with token
4. **Contact support** - Email ormcp_support@softwaretree.com

### Issue: Command Not Found

**Problem:** `ormcp-server: command not found` or `'ormcp-server' is not recognized`

**Solutions:**

**1. Find installation location:**
```bash
# Windows (PowerShell)
(Get-Command ormcp-server -ErrorAction SilentlyContinue).Source

# Windows (Command Prompt)
where ormcp-server

# Linux/Mac
which ormcp-server

# Any platform
pip show -f ormcp-server
```

**2. Add Scripts to PATH** (see platform-specific sections above)

**3. Use full path:**
```bash
# Windows
%APPDATA%\Python\Python313\Scripts\ormcp-server.exe

# Linux/Mac
~/.local/bin/ormcp-server
```

**4. Use Python module:**
```bash
python -m ormcp_server
```

### Issue: Empty Executable (0 bytes)

**Problem:** `ormcp-server.exe` is 0 bytes and won't run

**Solution:** Uninstall and reinstall:
```bash
pip uninstall ormcp-server

# Note: --extra-index-url is required for build dependencies
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server
```

This can happen due to antivirus interference during installation.

### Issue: Missing Dependencies

**Problem:** `ModuleNotFoundError: No module named 'requests'` or similar

**Solution:**
```bash
# Reinstall with dependencies
# Note: --extra-index-url is required for build dependencies
pip install --force-reinstall \
  --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server

# Or install missing dependency directly
pip install requests

# Verify all dependencies
pip show ormcp-server
# Check "Requires" line shows: fastmcp, httpx, mcp, pydantic, uvicorn, requests
```

### Issue: Build Dependencies Not Found

**Problem:** `ERROR: Could not find a version that satisfies the requirement hatchling` or similar build errors

**Solution:**

This happens when `--extra-index-url` is missing. Ensure you include it:

```bash
# Correct command with both flags
pip install --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server
```

Or configure pip permanently (see "Alternative: Configure pip Permanently" section above).

### Issue: SSL Certificate Error

**Problem:** SSL verification failed when connecting to Gemfury

**Solution:**
```bash
# Temporarily bypass SSL (not recommended for production)
pip install --trusted-host pypi.fury.io \
  --index-url https://YOUR_TOKEN@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  ormcp-server

# Better: Update certificates
pip install --upgrade certifi
```

---

## Next Steps

After installation:

1. **[Set up Gilhari Microservice](gilhari_setup.md)** - Required for ORMCP to function
2. **[Configure environment](quickstart.md#configuration)** - Set GILHARI_BASE_URL and other variables
3. **[Connect your AI client](quickstart.md#connect-ai-client)** - Configure Claude Desktop or other MCP client
4. **[Run your first query](quickstart.md#usage-examples)** - Test the installation

---

## Support

**Installation Issues:**
- Email: ormcp_support@softwaretree.com
- GitHub Issues: [Report a problem](https://github.com/softwaretree/ormcp-docs/issues)

**Beta Access:**
- Request token: [softwaretree.com/products/ormcp](https://www.softwaretree.com)

---

## Related Documentation

- [Back to Main README](../README.md)
- [Quick Start Guide](quickstart.md)
- [Gilhari Setup Guide](gilhari_setup.md)
- [Troubleshooting Guide](troubleshooting.md)