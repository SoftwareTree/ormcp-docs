#!/bin/bash
# start.sh
#
# Startup script for ORMCP Server in containerized environments.
# Used by Glama and other MCP registries to install and launch
# ORMCP Server with the required dependencies.
#
# ORMCP Server is installed from public PyPI; no access token is needed.
#
# Environment variables:
#   GILHARI_BASE_URL - URL of the Gilhari microservice, e.g.
#                      http://host.docker.internal:80/gilhari/v1/
#                      (required unless the default
#                      http://localhost:80/gilhari/v1/ is right)
#   GILHARI_IMAGE    - Optional: Docker image of the Gilhari microservice,
#                      if ORMCP should start it when none is running
#   READONLY_MODE    - Optional: "false" to expose the data-modification
#                      tools (default "true")
#
# Since ORMCP 0.7.0 the host and port for ORMCP's start-up check come from
# GILHARI_BASE_URL; GILHARI_HOST / GILHARI_PORT are only overrides.

uv venv /opt/venv && \
uv pip install ormcp-server --python /opt/venv/bin/python && \
mcp-proxy -- /opt/venv/bin/python -m ormcp_server
