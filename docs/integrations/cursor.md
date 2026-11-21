# Cursor IDE & Windsurf Integration

NexusPilot Cortex provides full MCP support for **Cursor IDE** and **Codeium Windsurf**.

---

## 1-Command Setup

```bash
# For Cursor IDE
npx nexus-pilot-cortex install --ide cursor

# For Windsurf
npx nexus-pilot-cortex install --ide windsurf
```

This updates:
* **Cursor:** `~/.cursor/mcp.json`
* **Windsurf:** `~/.codeium/windsurf/mcp_config.json`

---

## Manual MCP Configuration

In Cursor or Windsurf MCP settings:

```json
{
  "mcpServers": {
    "nexus-pilot-cortex": {
      "command": "npx",
      "args": ["-y", "nexus-pilot-cortex"]
    }
  }
}
```
Reload your editor window to activate the tools.
