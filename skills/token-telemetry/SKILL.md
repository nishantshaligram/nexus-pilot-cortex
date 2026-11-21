---
name: token-telemetry
description: Real-time token usage telemetry, cost estimation, prompt cache hit rate tracking, and per-response badge generation for Google Antigravity.
---

# Token Telemetry & Per-Response Badging

This skill provides real-time visibility into LLM token consumption, prompt cache efficiency, generation speeds, and operational costs.

## When to Use
- Appending the per-response token telemetry badge to user turns.
- Inspecting session or workspace token spend and budget headroom.
- Auditing prompt caching performance across multi-turn workflows.

## Key Tools
- `render_telemetry_badge(input_tokens, cached_tokens, output_tokens, model, mode)`: Formats standard or detailed badge.
- `record_turn_telemetry(...)`: Logs usage to the session ledger and computes USD costs.
- `get_telemetry_stats()`: Returns cumulative statistics for the conversation.
- `estimate_tokens(text)`: Estimates token count for text or code blocks.

## Badge Formatting Examples
* **Standard Compact:**
  `Token Telemetry: In: 3.1k | Cache: 83.7k | Out: 225 | Total: 87.0k`
* **Detailed Mode:**
  `📊 NexusPilot | In: 3.1k | Cache: 83.7k (96.4% hit) | Out: 225 | Speed: 187 tok/s | Cost: $0.0018`
