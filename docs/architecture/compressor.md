# Architecture: Context & capacity Compressor

The Compressor brings **adaptive context compression** to Antigravity, eliminating context cliffs, minimizing prompt tokens, and maximizing Gemini prefix caching hit rates.

---

## Output Compaction Strategies

When command-line tools generate megabytes of verbose output, Cortex applies multi-stage lossless/near-lossless compression:

1. **Repeated Log Line Collapsing:**
   Converts repeated log bursts:
   ```text
   Error: connection timeout
   Error: connection timeout
   [... 40 identical lines ...]
   ```
   Into:
   ```text
   Error: connection timeout
     ... [repeated 42 times] ...
   ```

2. **Framework Stack Frame Folding:**
   Collapses external framework internals (`node_modules`, `site-packages`, standard runtime libraries) while strictly preserving user application frames and root causes.

3. **Git Diff Cleaning:**
   Removes git index hashes, blob metadata, and empty hunks, presenting clean code deltas.

4. **Windowed Ellipses:**
   If tool output exceeds the maximum token budget, Cortex preserves the top 60% and tail 40% with an explicit notification notice.

---

## Gemini Prefix Cache Optimization

Prefix caching relies on static prompt prefixes remaining strictly unchanged across conversation turns.

```text
[Optimal Cache Layout]
┌──────────────────────────────────────────────┐
│ Tier 1: System Rules & Plugin Declarations   │ <- Locked Prefix (Cached)
├──────────────────────────────────────────────┤
│ Tier 2: Workspace Conventions & Memories     │ <- Semi-Static (Cached)
├──────────────────────────────────────────────┤
│ Tier 3: Conversation History                 │ <- Incremental Turns
├──────────────────────────────────────────────┤
│ Tier 4: Latest User Query & Tool Outputs     │ <- Dynamic Tail
└──────────────────────────────────────────────┘
```

Cortex’s `validate_prefix_ordering` verifies that dynamic content is never injected ahead of static rules, preserving **85% to 95%+ prompt cache hit ratios**.
