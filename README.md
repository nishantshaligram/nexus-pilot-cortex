# NexusPilot: Cortex 🧠⚡

**Cognitive Telemetry, Memory Management & Context Compression Engine for Google Antigravity**  
*Part of the NexusPilot Autonomous Agent Suite*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-brightgreen.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](#)
[![Suite](https://img.shields.io/badge/Suite-NexusPilot-purple.svg)](#)

---

## 🌟 Overview

`NexusPilot: Cortex` is the cognitive middleware for Antigravity agents. While **NexusPilot Desktop** acts as the agent's hands (GUI and Windows UI automation), **Cortex** acts as its brain and efficiency governor, delivering three foundational capabilities:

1. **Per-Response Token Telemetry & Badging:** Instant visibility into input prompt tokens, cached tokens, output tokens, total tokens, latency, generation speed, and estimated USD cost.
2. **Autonomous Long-Term Memory (*claude-mem* parity):** Persistent local SQLite memory that automatically learns user preferences, project conventions, and negative constraints across sessions.
3. **Adaptive Context & Output Compressor (*headroom* parity):** Collapses repetitive logs, folds vendor stack frames, and enforces Gemini prefix caching alignment to eliminate context cliffs and save 35–65% of billed tokens.

---

## 🚀 The Three Pillars

### 1. Token Telemetry & Per-Response Badging
Appends a clean badge to the end of each completion turn:
```text
Token Telemetry: In: 3.1k | Cache: 83.7k | Out: 225 | Total: 87.0k
```
* **Detailed Mode:**
  ```text
  > 📊 NexusPilot Telemetry | In: 3.1k | Cache: 83.7k (96.4% hit) | Out: 225 | Speed: 187 tok/s | Cost: $0.0018
  ```
* **Live Pricing:** Tracks costs against current Gemini 1.5/2.0, Claude 3.5 Sonnet, and GPT-4o pricing tiers.

### 2. Autonomous Memory Governor (*"claude-mem"*)
* **Multi-Tiered Memory:** Organizes knowledge into `preference`, `architecture`, `episodic`, and `constraint`.
* **Zero-Shot Fact Extraction:** Heuristic extractor automatically detects statements like *"Always use pnpm"*, *"Our DB is Postgres on port 5432"*, or *"Never touch legacy directory `v1/`"*.
* **Semantic Retrieval & Pinned Boost:** BM25 keyword matching with recency decay prioritizes critical conventions and injects them into Antigravity context.

### 3. Context & Headroom Compressor (*"headroom"*)
* **Output Compaction:** Collapses redundant logs (`... [repeated 42 times] ...`), folds external stack traces (`node_modules`, `site-packages`), and cleans git diffs.
* **Gemini Prefix Cache Aligner:** Preserves cache breakpoints by ensuring static system rules precede dynamic session turns, achieving **85–95%+ cache hit rates**.
* **Headroom Cliff Guard:** Monitored headroom triggers proactive consolidation before hitting token thresholds.

---

## 📦 Directory Structure

```text
nexus-pilot-cortex/
├── plugin.json                 # Antigravity Plugin Manifest
├── mcp_config.json             # MCP Server configuration
├── README.md                   # Documentation
├── requirements.txt            # Optional dependencies
├── install-cortex.bat          # 1-Click Windows installer
├── assets/
│   └── logo.svg                # Plugin vector emblem
├── rules/
│   └── AGENTS.md               # Behavioral rules for Antigravity agents
├── skills/
│   ├── token-telemetry/        # Telemetry & badge inspection
│   ├── memory-governor/        # Memory search, recall, and persistence
│   └── context-compressor/     # Context pruning and headroom governor
├── server/
│   ├── cortex_server.py        # Central FastMCP/MCPServer entry point
│   ├── telemetry/              # Turn counter, pricing calculator, badge renderer
│   ├── memory/                 # SQLite storage, autonomous extractor, BM25 retriever
│   └── compressor/             # Log collapser, stack trace folder, cache aligner
├── tests/
│   ├── run_tests.py            # Standard library test runner (0 dependencies)
│   └── test_cortex.py          # Pytest test suite
└── scripts/
    └── install-cortex.ps1      # PowerShell linking & registration script
```

---

## 🛠️ Installation & NPX CLI

`NexusPilot: Cortex` implements the **Zero-Config Node.js $\rightarrow$ Python Bootstrapper pattern**, allowing 1-command execution and installation via `npx` with zero manual git clones or JSON editing:

### 1. Direct Agent MCP Integration (Zero Installation)
In any AI agent's configuration (`~/.claude.json`, `mcp.json`, etc.), you can invoke Cortex directly via `npx`:
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

### 2. 1-Command CLI Installer (`npx`)
```bash
# Interactive multi-agent installer (Antigravity, Claude, Cursor, Windsurf)
npx nexus-pilot-cortex install

# Targeted agent installation
npx nexus-pilot-cortex install --agent antigravity
npx nexus-pilot-cortex install --agent claude
npx nexus-pilot-cortex install --ide cursor
```

### 3. Environment & SQLite Diagnostic Probe
```bash
npx nexus-pilot-cortex doctor
```

### 4. Windows 1-Click Interactive Batch Installer
Alternatively, double-click `install-cortex.bat` (or `install-agents.bat`):
```cmd
:: Install with specific target flags
install-cortex.bat -Antigravity
install-cortex.bat -Claude
install-cortex.bat -Target "Antigravity, Claude"
```

### Running the Test Suite
Cortex requires zero external pip dependencies to run:
```bash
python tests/run_tests.py -v
```

---

## 🔧 Exposed MCP Tools

| Tool | Category | Description |
| :--- | :--- | :--- |
| `render_telemetry_badge` | Telemetry | Generates formatted `Token Telemetry: In: ...` badge |
| `record_turn_telemetry` | Telemetry | Records turn metrics and calculates USD cost & speed |
| `get_telemetry_stats` | Telemetry | Cumulative conversation tokens, cost, and cache hit % |
| `estimate_tokens` | Telemetry | Pre-flight token estimator for text blocks |
| `search_memories` | Memory | Retrieves stored conventions matching query |
| `remember_fact` | Memory | Explicitly stores a persistent memory node |
| `forget_memory` | Memory | Deletes an outdated memory node by ID |
| `auto_extract_and_remember`| Memory | Scans text for learnable patterns automatically |
| `get_memory_context_injection`| Memory | Returns formatted markdown block for prompt context |
| `compress_tool_output` | Compression | Collapses noisy CLI logs, stack traces, and diffs |
| `check_context_headroom` | Compression | Evaluates remaining context capacity and cliff warnings |
| `check_cortex_health` | Diagnostic | Returns engine status, DB path, and memory count |

---

## 🤝 NexusPilot Suite Integration

| Component | Role | Description |
| :--- | :--- | :--- |
| **`nexus-pilot`** | Hands | Computer-Use, Windows UI Automation, Vision, Foreground HUD |
| **`nexus-pilot-cortex`** | Brain | Telemetry, Memory Governor, Headroom Context Compression |
| **`nexus-pilot-phantomcorp`** | Shadow | Headless Background Workers, Synthetic QA & Security Swarms |
| **`nexus-pilot-fleet`** | Grid | Distributed Swarm Orchestrator, DAG Scheduler, Worktree Multiplexing |

---

## 📄 License
MIT License. Part of Project NexusPilot.
