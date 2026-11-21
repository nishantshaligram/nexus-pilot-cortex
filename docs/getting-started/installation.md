# Installation Guide

NexusPilot Cortex supports multiple zero-friction installation pathways depending on your preferred workflow.

---

## 1. Zero-Install NPX Execution

You can integrate Cortex directly into any AI agent without cloning the repo:

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

---

## 2. 1-Command CLI Installer

To install plugins, skills, and configuration into your local AI agents:

```bash
# Interactive selection
npx nexus-pilot-cortex install

# Or target specific agents directly
npx nexus-pilot-cortex install --agent antigravity
npx nexus-pilot-cortex install --agent claude
npx nexus-pilot-cortex install --ide cursor
npx nexus-pilot-cortex install --ide windsurf
```

---

## 3. Windows 1-Click Interactive Batch Installer

If working from source on Windows:
```cmd
:: Launch interactive installer
install-cortex.bat

:: Or pass targeted environment flags
install-cortex.bat -Antigravity
install-cortex.bat -Claude
install-cortex.bat -Target "Antigravity, Cursor"
```

---

## 4. Diagnostic Health Check

Verify your Python environment, SQLite database, and dependencies at any time:

```bash
npx nexus-pilot-cortex doctor
```
