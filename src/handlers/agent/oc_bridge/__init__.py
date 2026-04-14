"""
OC Bridge — MCP client integration with OpenClaw.

Provides two MCP channels:
  - Channel MCP (openclaw mcp serve): conversation-level delegation
  - Plugin Tools MCP (plugin-tools-serve): direct memory/tool access

All components gracefully degrade when OpenClaw is unavailable.
"""
