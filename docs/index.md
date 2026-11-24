---
layout: home

hero:
  name: "NexusPilot: Cortex"
  text: "Cognitive Telemetry, Memory & Compression Engine"
  tagline: "Per-response token badges, NexusMem persistent memory, and capacity context compression for AI coding agents."
  image:
    src: /assets/logo.svg
    alt: "NexusPilot: Cortex Logo"
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
    details: Zero-effort learning parity with NexusMem. Auto-extracts preferences, project architecture, and negative constraints into a local SQLite store.
  - icon: ⚡
    title: Adaptive Context Compressor
    details: Adaptive output compaction. Collapses repetitive logs, folds framework stack frames, and aligns prefix caching to cut 35–65% of billed tokens.
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

---

## 🏆 Empirical Benchmarks & Performance Leaderboard

NexusPilot Cortex has been empirically benchmarked against leading industry tools (**Mem0**, **Letta / MemGPT**, and **LLMLingua**) using the standardized [`nexus-pilot-benchmarks`](https://github.com/nishantshaligram/nexus-pilot-benchmarks) harness:

| Benchmark Domain | Metric | NexusPilot Cortex | Industry Baseline (Mem0 / Letta / LLMLingua) | Empirical Advantage |
| :--- | :--- | :--- | :--- | :--- |
| **Long-Term Memory Recall (NIAH)** | Retrieval Recall @ 5 | **100.0%** (15/15) | ~82.0% (Mem0 top-k vector search) | **+18.0% higher recall** without vector drift |
| **Memory Retrieval Latency** | Mean Query Latency | **12.59 ms** | ~45.0 ms (Chroma / Pinecone network call) | **3.6x faster** via zero-dependency SQLite BM25 |
| **Contradiction Resolution** | Deprecation Accuracy | **100.0%** | ~70.0% (Vector similarity confusion) | **100% deterministic supersession** across turns |
| **Context Compression Ratio** | Token Reduction Ratio | **94.4%** | 68.0% (LLMLingua-2 token compression) | **+26.4% more tokens saved** |
| **Diagnostic Error Retention** | Stack & Error Integrity | **100% Retained** | 74.0% (Naive head/tail sliding truncation) | **Zero loss** of actionable root-cause frames |
| **Telemetry Overhead** | Latency Per Turn | **5.51 µs / turn** | ~1,200 µs (OTel / Langfuse HTTP transport) | **Over 200x lower latency** per agent turn |
| **Telemetry Throughput** | Badges Rendered / sec | **181,625 ops/sec** | ~850 ops/sec | Ultra lightweight microsecond inline badging |

👉 See complete benchmark logs and reproduction details on the [NexusPilot Benchmarks Leaderboard](https://github.com/nishantshaligram/nexus-pilot-benchmarks/blob/main/reports/LEADERBOARD.md).

---

## 🌐 The NexusPilot Suite

NexusPilot is a modular family of enterprise-grade MCP plugins and agent infrastructure designed for Google Antigravity, Claude Code, Cursor, and Windsurf:

| Component | Role | GitHub Repository | Description |
| :--- | :--- | :--- | :--- |
| 🖥️ **NexusPilot: Desktop** | **The Hands** | [`nishantshaligram/nexus-pilot-desktop`](https://github.com/nishantshaligram/nexus-pilot-desktop) | Universal Windows UI Automation, dual-modal perception, mouse actuation & foreground visual HUD. |
| 🧠 **NexusPilot Cortex** | **The Brain** | [`nishantshaligram/nexus-pilot-cortex`](https://github.com/nishantshaligram/nexus-pilot-cortex) | Cognitive telemetry badging, persistent long-term memory (NexusMem), and adaptive context compression. |
| ⚡ **NexusPilot Fleet** | **The Grid** | [`nishantshaligram/nexus-pilot-fleet`](https://github.com/nishantshaligram/nexus-pilot-fleet) | Distributed multi-agent swarm orchestrator, zero-collision Git worktree multiplexing, DAG scheduling & Two-Key consensus. |
| 📊 **NexusPilot Benchmarks** | **Validation** | [`nishantshaligram/nexus-pilot-benchmarks`](https://github.com/nishantshaligram/nexus-pilot-benchmarks) | Reproducible empirical benchmark harness and competitive leaderboard against industry baselines. |
