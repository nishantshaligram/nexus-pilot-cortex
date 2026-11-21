---
layout: home

hero:
  name: "NexusPilot Cortex"
  text: "Cognitive Telemetry, Memory & Compression Engine"
  tagline: "Per-response token badges, claude-mem persistent memory, and headroom context compression for AI coding agents."
  image:
    src: /assets/logo.svg
    alt: NexusPilot Cortex Logo
  actions:
    - theme: brand
      text: Get Started
      link: /getting-started/quickstart
    - theme: alt
      text: MCP Tool Catalog
      link: /reference/mcp-tools
    - theme: alt
      text: View on GitHub
      link: https://github.com/nishantshaligram/nexus-pilot-cortex

features:
  - icon: 📊
    title: Real-Time Token Telemetry Badges
    details: Instant visibility into prompt tokens, cached tokens, completion tokens, latency, speed (tok/s), and real-time USD cost on every turn.
  - icon: 🧠
    title: Autonomous Long-Term Memory
    details: Zero-effort learning parity with claude-mem. Auto-extracts preferences, project architecture, and negative constraints into a local SQLite store.
  - icon: ⚡
    title: Adaptive Context Compressor
    details: Headroom-style output compaction. Collapses repetitive logs, folds framework stack frames, and aligns prefix caching to cut 35–65% of billed tokens.
  - icon: 🌐
    title: Multi-Agent & IDE Ecosystem
    details: Universal support for Google Antigravity, Claude Code, Claude Desktop, Cursor IDE, Windsurf, and any standard MCP client.
---

## Why NexusPilot Cortex?

Modern AI agents face three major performance and economic bottlenecks:

1. **Context Window Amnesia:** Agents lose project conventions and user preferences across conversation restarts.
2. **Context Bloat & Token Cliffs:** Massive terminal logs, deep stack traces, and noisy git diffs burn thousands of tokens and degrade reasoning.
3. **Opaque Operational Cost:** Developers have no per-turn feedback on prompt cache efficiency and real-time spending.

**NexusPilot Cortex** acts as the cognitive governor that solves all three seamlessly with **100% local-first storage** and **zero required external dependencies**.
