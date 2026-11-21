---
name: memory-governor
description: Persistent cross-session and cross-workspace memory management (claude-mem parity), autonomous fact learning, and progressive context injection.
---

# Memory Governor

This skill provides persistent long-term memory for Antigravity agents, allowing them to recall user preferences, architectural decisions, and project conventions across sessions without manual re-prompting.

## When to Use
- Recalling stored conventions before generating code or modifying system configurations.
- Storing new technical decisions, user preferences, or negative constraints.
- Cleaning up outdated memories or pinning critical directives.

## Memory Taxonomy
1. **User Persona & Preferences:** Tool choices, styling guidelines, tone preferences.
2. **Project Architecture:** Frameworks, database ports, directory structures, build tools.
3. **Episodic Learnings:** Specific bug workarounds and resolution notes.
4. **Negative Constraints:** Explicit prohibitions ("Do not run npm without pnpm wrapper").

## Key Tools
- `search_memories(query, workspace_uri, limit)`: Semantic BM25 + recency ranking.
- `remember_fact(fact, subject, category, scope, pinned)`: Explicit fact storage.
- `auto_extract_and_remember(text)`: Autonomous zero-shot extraction.
- `forget_memory(memory_id)`: Deletes an obsolete memory node.
- `get_memory_context_injection(query)`: Formatted markdown injection.
