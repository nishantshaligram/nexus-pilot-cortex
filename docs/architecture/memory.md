# Architecture: Autonomous Memory Engine

The Memory Engine brings **NexusMem autonomous persistence** to open AI agents, enabling cross-session persistence, automatic fact extraction, and progressive context injection.

---

## Memory Taxonomy

Cortex stores knowledge across four functional tiers:

1. **`preference`:** User styling rules, favorite package managers, tone directives.
2. **`architecture`:** Tech stack, database ports, service directory layouts, reserved endpoints.
3. **`episodic`:** Bug workarounds, past incident resolutions, migration notes.
4. **`constraint`:** Negative guardrails ("Never run tests without coverage flag", "Do not touch legacy v1 endpoints").

---

## Zero-Shot Fact Extractor

The extractor (`server/memory/extractor.py`) scans user prompts and conversation turns using natural language heuristics:
* **Preference Detection:** `"always use X"`, `"prefer Y"`, `"from now on use Z"`
* **Constraint Detection:** `"never use X"`, `"do not run Y"`, `"avoid Z"`
* **Architecture Detection:** `"our database is X"`, `"server listens on port Y"`
* **Explicit Memorization:** `"remember that X"`, `"keep in mind that Y"`

---

## Storage & Ranking Schema

Stored locally in an embedded SQLite database (`cortex_memory.db`):

```sql
CREATE TABLE memories (
    id TEXT PRIMARY KEY,
    scope TEXT NOT NULL CHECK(scope IN ('global', 'workspace')),
    workspace_uri TEXT,
    category TEXT NOT NULL CHECK(category IN ('preference', 'architecture', 'episodic', 'constraint')),
    subject TEXT NOT NULL,
    fact TEXT NOT NULL,
    keywords TEXT,
    confidence REAL DEFAULT 1.0,
    pinned INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    access_count INTEGER DEFAULT 0
);
```

### Ranking & Scoring Function
When an agent queries for context, memories are scored using:
$$\text{Score} = (\text{Keyword Overlap} \times 2.0 + \text{Pinned Bonus}) \times \text{Recency Multiplier}$$

Where:
* **Pinned Bonus:** $+5.0$ if memory is marked `pinned: 1`.
* **Recency Decay:** Decays linearly over 30 days to prioritize freshly accessed conventions.
