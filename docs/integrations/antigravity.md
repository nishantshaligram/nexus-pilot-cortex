# Google Antigravity Integration

NexusPilot Cortex is designed as a native first-class plugin for Google Antigravity.

---

## Automatic Installation

To install Cortex into Antigravity:
```bash
npx nexus-pilot-cortex install --agent antigravity
```
Or run the batch installer:
```cmd
install-cortex.bat -Antigravity
```

This copies the plugin bundle to:
`~/.gemini/config/plugins/nexus-pilot-cortex/`

---

## Bundled Antigravity Skills

| Skill | Directory | Description |
| :--- | :--- | :--- |
| `token-telemetry` | `skills/token-telemetry/` | Real-time token usage, per-response badge generation, and cost auditing. |
| `memory-governor` | `skills/memory-governor/` | Semantic memory recall, zero-shot fact extraction, and context injection. |
| `context-compressor` | `skills/context-compressor/` | Log folding, stack frame reduction, and headroom management. |

---

## Behavioral Rules

Cortex injects rules from `rules/AGENTS.md` to ensure agents automatically:
- Append token badges at the end of substantive turns.
- Search relevant project memories before executing major tasks.
- Compress tool outputs exceeding 100 lines.
