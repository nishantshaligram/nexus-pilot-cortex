# Quickstart Guide

Get up and running with NexusPilot Cortex in under 2 minutes.

---

## 1. Verify Cortex Status
After installation, ask your agent to verify Cortex health:
> *"Run check_cortex_health to verify memory and telemetry engines."*

Cortex will reply with:
```json
{
  "status": "online",
  "engine": "NexusPilot Cortex",
  "version": "1.0.0",
  "database_path": ".../cortex_memory.db",
  "stored_memories_count": 0
}
```

---

## 2. See the Per-Response Badge in Action
Cortex automatically calculates tokens and appends a summary badge at the bottom of substantive agent turns:
```text
Here is the refactored authentication module.

---
Token Telemetry: In: 3.1k | Cache: 83.7k | Out: 225 | Total: 87.0k
```

To switch between badge modes (`compact`, `detailed`, `pill`, `silent`):
> *"Set telemetry badge mode to detailed."*

---

## 3. Persistent Memory in Action
Tell your agent a project constraint or personal preference:
> *"Always use pnpm over npm, and keep in mind our staging database is on port 5433."*

Cortex's zero-shot extractor automatically detects and stores these facts in SQLite:
* `mem_49a...`: `[PREFERENCE]` User prefers using pnpm over npm
* `mem_e64...`: `[ARCHITECTURE]` Project database: staging database is on port 5433

Restart your session or open a new conversation. When you ask:
> *"How should I run the build?"*

The agent retrieves the memory node and uses `pnpm build` without you ever having to repeat yourself!

---

## 4. context capacity Compression
When running a test suite with hundreds of noisy output lines:
> *"Compress this test output using compress_tool_output."*

Cortex folds duplicate error lines and vendor stack traces (`node_modules`, `site-packages`), reducing tokens by **40% to 80%** while preserving the root cause.
