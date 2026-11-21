# NexusPilot Cortex - Cognitive Engine Directives

These directives govern agent memory management, token telemetry badging, and context compression across all Antigravity interactions.

## Rule 1: Per-Response Token Telemetry Badge
- At the conclusion of every substantive response turn, append a concise token telemetry summary badge formatted as:
  ```text
  Token Telemetry: In: <in_tokens> | Cache: <cache_tokens> | Out: <out_tokens> | Total: <total_tokens>
  ```
- If active metrics from the server tool `render_telemetry_badge` are available, use them. If running in offline estimation mode, estimate turn tokens using the heuristic (~3.8 characters per token) and model prefix cache status.

## Rule 2: Memory-First Autonomous Recall
- At the start of a task or when answering architectural questions, check recalled memories using `search_memories(query=...)`.
- Prioritize pinned preferences and project conventions over generic defaults.
- Never violate stored negative constraints (e.g., prohibited tools, protected branches, or deprecated endpoints).

## Rule 3: Autonomous Zero-Effort Learning
- When a user corrects a mistake or declares a preference (e.g., *"Always use pnpm"*, *"Our DB is Postgres 16"*), immediately record it using `remember_fact(...)` or `auto_extract_and_remember(...)`.
- Acknowledge remembered facts concisely without cluttering the conversation.

## Rule 4: High-Entropy Output Compaction (Context Headroom)
- When capturing or relaying large tool outputs (test suites, stack traces, compiler errors, large JSON dumps, git diffs), use `compress_tool_output(...)` to fold vendor frames and collapse repetitive errors.
- Never flood the context window with raw dumps exceeding 100 lines without summarization.
