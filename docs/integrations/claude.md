# Claude Integration (Code CLI & Desktop)

NexusPilot Cortex integrates with both **Claude Code CLI** and the **Claude Desktop App**.

---

## 1-Command Setup

```bash
npx nexus-pilot-cortex install --agent claude
```
Or via Windows batch:
```cmd
install-cortex.bat -Claude
```

This configures:
* **Claude Code CLI:** `~/.claude.json`
* **Claude Desktop App:** `%APPDATA%\Claude\claude_desktop_config.json`

---

## Manual MCP Configuration

If you prefer to configure manually, add the following to your Claude config:

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
*(Or use `python` with the direct path to `server/cortex_server.py`).*
