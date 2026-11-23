---
name: context-compressor
description: Adaptive context compression (Adaptive Context Compression), tool output reduction, stack trace folding, and prefix cache alignment for Antigravity.
---

# Context Compressor & capacity governor

This skill protects the context window from token bloat, reduces inference costs, and maintains high prompt cache hit ratios.

## When to Use
- Compacting large command line outputs (e.g., test runner logs, compiler output, stack traces).
- Checking remaining token capacity before initiating long multi-agent chains.
- Restructuring prompt context to preserve Gemini / Antigravity prefix caching.

## Compression Strategies
1. **Repeated Log Line Collapsing:** Replaces repeated error lines with `... [repeated N times] ...`.
2. **Framework Stack Trace Folding:** Collapses vendor frames (`node_modules`, `site-packages`) while preserving workspace application code lines.
3. **Diff Cleaning:** Strips git commit hashes and metadata headers.
4. **Windowed Ellipses:** Protects context by preserving top 60% and tail 40% with a clean omission notice.

## Key Tools
- `compress_tool_output(raw_output, max_chars)`: Compresses noisy outputs.
- `check_context_budget(current_tokens, context_limit)`: Returns SAFE, WARNING, or CRITICAL status.
