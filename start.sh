#!/bin/bash
# start.sh
# 
# Startup script for ORMCP Server in containerized environments.
# Used by Glama and other MCP registries to install and launch 
# ORMCP Server with the required dependencies.
#
# Required environment variables:
#   GEMFURY_TOKEN   - Beta access token for installing ormcp-server
#   GILHARI_IMAGE   - Docker image for the Gilhari microservice
#   GILHARI_HOST    - Host for Gilhari (use host.docker.internal in Docker)
#   GILHARI_PORT    - Port for Gilhari microservice (default: 80)
#   GILHARI_BASE_URL - Full URL for Gilhari microservice

uv venv /opt/venv && \
uv pip install ormcp-server \
  --index-url https://${GEMFURY_TOKEN}@pypi.fury.io/softwaretree/ \
  --extra-index-url https://pypi.org/simple \
  --python /opt/venv/bin/python && \
mcp-proxy -- /opt/venv/bin/python -m ormcp_server
