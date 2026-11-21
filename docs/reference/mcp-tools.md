# MCP Tool Catalog

NexusPilot Cortex exposes 12 specialized tools across Telemetry, Memory, and Context Compression.

---

## 📊 Telemetry Tools

### `render_telemetry_badge`
Generates a formatted token telemetry badge string ready to append at the bottom of agent responses.
* **Parameters:**
  * `input_tokens` (integer, required)
  * `cached_tokens` (integer, required)
  * `output_tokens` (integer, required)
  * `model` (string, optional, default: `"gemini-2.0-flash"`)
  * `mode` (string, optional: `"compact"`, `"detailed"`, `"pill"`, `"silent"`)

### `record_turn_telemetry`
Records turn consumption in the session ledger and computes USD costs, speed, and cache hit rates.

### `get_telemetry_stats`
Returns cumulative session metrics (total input/cached/output tokens, average cache hit %, total cost, duration).

### `estimate_tokens`
Estimates token count for a text string prior to calling high-token tools.

---

## 🧠 Memory Tools

### `search_memories`
Searches persistent memories matching a query using hybrid BM25 scoring, recency decay, and pinned status.
* **Parameters:**
  * `query` (string, required)
  * `workspace_uri` (string, optional)
  * `limit` (integer, optional, default: `5`)

### `remember_fact`
Saves or updates a persistent memory node.
* **Parameters:**
  * `fact` (string, required)
  * `subject` (string, optional)
  * `category` (string, required: `"preference"`, `"architecture"`, `"episodic"`, `"constraint"`)
  * `scope` (string, optional: `"global"`, `"workspace"`)
  * `pinned` (boolean, optional, default: `false`)

### `forget_memory`
Deletes a memory node by ID.

### `auto_extract_and_remember`
Scans a prompt or turn text for conventions, tech stack specs, and constraints, automatically persisting them to SQLite.

### `get_memory_context_injection`
Generates a formatted markdown block of relevant memories ready for context inclusion.

---

## ⚡ Context Compression Tools

### `compress_tool_output`
Collapses repeated lines, folds framework stack frames, and trims git diffs.
* **Parameters:**
  * `raw_output` (string, required)
  * `max_chars` (integer, optional, default: `4000`)

### `check_context_headroom`
Evaluates remaining token headroom against context ceilings and returns `"SAFE"`, `"WARNING"`, or `"CRITICAL"`.

### `check_cortex_health`
Diagnostic probe returning engine status, SQLite DB path, memory count, and session spend.
