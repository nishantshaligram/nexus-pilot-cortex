"""
NexusPilot Cortex - Model Context Protocol (MCP) Server
Unified Cognitive Engine for Antigravity:
1. Token Telemetry & Per-Response Badging
2. Persistent Autonomous Memory (claude-mem parity)
3. Adaptive Context & Tool Output Compression (headroom parity)
"""

import sys
import os
from typing import Optional, List, Dict, Any

# Ensure current directory is on path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

from telemetry import TelemetryTracker, TokenMetrics, estimate_token_count, render_badge
from memory import MemoryStore, MemoryDatabase
from compressor import compress_output, CacheAndHeadroomAligner

try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP as MCPServer
    except ImportError:
        raise RuntimeError("mcp Python SDK is required. Run 'pip install mcp'")

# Instantiate core engines
telemetry_tracker = TelemetryTracker()
memory_store = MemoryStore()
headroom_aligner = CacheAndHeadroomAligner()

server = MCPServer("nexus-pilot-cortex")


# ==============================================================================
# Pillar 1: Telemetry & Per-Response Badging Tools
# ==============================================================================

@server.tool()
def render_telemetry_badge(
    input_tokens: int,
    cached_tokens: int,
    output_tokens: int,
    model: str = "gemini-2.0-flash",
    mode: str = "compact"
) -> str:
    """
    Generates a concise token telemetry badge to append at the bottom of agent responses.
    Modes:
      - 'compact': 'Token Telemetry: In: 3.1k | Cache: 83.7k | Out: 225 | Total: 87.0k'
      - 'detailed': Includes cost, generation speed, and percentage cache hit.
      - 'pill': Markdown quote block with highlighted metrics.
      - 'silent': Empty string.
    """
    metrics = telemetry_tracker.record_turn(
        input_tokens=input_tokens,
        cached_tokens=cached_tokens,
        output_tokens=output_tokens,
        model=model
    )
    return render_badge(metrics, mode=mode)


@server.tool()
def record_turn_telemetry(
    input_tokens: int,
    cached_tokens: int,
    output_tokens: int,
    latency_ms: int = 500,
    model: str = "gemini-2.0-flash"
) -> dict:
    """
    Records a turn's token consumption in the session ledger and computes
    prompt cache hit rate, generation speed, and estimated USD cost.
    """
    metrics = telemetry_tracker.record_turn(
        input_tokens=input_tokens,
        cached_tokens=cached_tokens,
        output_tokens=output_tokens,
        latency_ms=latency_ms,
        model=model
    )
    return metrics.to_dict()


@server.tool()
def get_telemetry_stats() -> dict:
    """
    Returns cumulative session telemetry statistics:
    total tokens, prompt cache hit rate, total cost (USD), and session duration.
    """
    return telemetry_tracker.get_session_summary()


@server.tool()
def estimate_tokens(text: str) -> dict:
    """
    Estimates the number of tokens in a provided text string.
    Useful for budgeting context headroom prior to calling large tools.
    """
    count = estimate_token_count(text)
    return {
        "estimated_tokens": count,
        "character_count": len(text)
    }


# ==============================================================================
# Pillar 2: Autonomous Memory Management Tools (claude-mem parity)
# ==============================================================================

@server.tool()
def search_memories(
    query: str,
    workspace_uri: Optional[str] = None,
    limit: int = 5
) -> list:
    """
    Searches persistent memories matching the query using keyword/BM25 scoring,
    recency decay, and pinned status.
    """
    return memory_store.search_relevant_memories(
        query=query,
        workspace_uri=workspace_uri,
        limit=limit
    )


@server.tool()
def remember_fact(
    fact: str,
    subject: str = "general",
    category: str = "preference",
    scope: str = "workspace",
    workspace_uri: Optional[str] = None,
    pinned: bool = False
) -> dict:
    """
    Saves a persistent fact, convention, preference, or negative constraint to memory.
    Category must be one of: 'preference', 'architecture', 'episodic', 'constraint'.
    Scope must be: 'global' or 'workspace'.
    """
    mem_id = memory_store.record_manual_fact(
        fact=fact,
        subject=subject,
        category=category,
        scope=scope,
        workspace_uri=workspace_uri,
        pinned=pinned
    )
    return {
        "status": "remembered",
        "memory_id": mem_id,
        "fact": fact,
        "category": category,
        "pinned": pinned
    }


@server.tool()
def forget_memory(memory_id: str) -> dict:
    """
    Removes a persistent memory by ID.
    """
    success = memory_store.db.delete_memory(memory_id)
    return {
        "status": "deleted" if success else "not_found",
        "memory_id": memory_id
    }


@server.tool()
def auto_extract_and_remember(
    text: str,
    scope: str = "workspace",
    workspace_uri: Optional[str] = None
) -> dict:
    """
    Scans a conversation turn or user statement for preferences, technical stack choices,
    or negative constraints and automatically saves high-confidence facts to memory.
    """
    mem_ids = memory_store.auto_learn_from_interaction(
        user_input=text,
        scope=scope,
        workspace_uri=workspace_uri
    )
    return {
        "extracted_count": len(mem_ids),
        "saved_memory_ids": mem_ids
    }


@server.tool()
def get_memory_context_injection(
    query: str,
    workspace_uri: Optional[str] = None,
    limit: int = 4
) -> str:
    """
    Generates a concise markdown snippet of relevant memories for inclusion
    in the active context window.
    """
    return memory_store.generate_context_injection(
        query=query,
        workspace_uri=workspace_uri,
        limit=limit
    )


# ==============================================================================
# Pillar 3: Context & Headroom Compressor Tools (headroom parity)
# ==============================================================================

@server.tool()
def compress_tool_output(
    raw_output: str,
    max_chars: int = 4000
) -> dict:
    """
    Compresses large tool outputs (terminal logs, stack traces, diffs, JSON)
    by collapsing repeated lines, folding vendor stack frames, and pruning noise.
    Returns the compressed text and token/character reduction metrics.
    """
    compressed_text, metrics = compress_output(raw_output, max_chars=max_chars)
    return {
        "compressed_output": compressed_text,
        "metrics": metrics
    }


@server.tool()
def check_context_headroom(
    current_tokens: int,
    context_limit: int = 1_000_000
) -> dict:
    """
    Evaluates remaining token headroom against model context limit.
    Flags warning thresholds and provides actionable recommendations to prevent context cutoff.
    """
    aligner = CacheAndHeadroomAligner(context_limit=context_limit)
    return aligner.check_headroom(current_tokens)


@server.tool()
def check_cortex_health() -> dict:
    """
    Health check returning status of Telemetry, Memory, and Compressor engines.
    """
    all_mems = memory_store.db.list_all()
    stats = telemetry_tracker.get_session_summary()
    return {
        "status": "online",
        "engine": "NexusPilot Cortex",
        "version": "1.0.0",
        "database_path": memory_store.db.db_path,
        "stored_memories_count": len(all_mems),
        "session_turns_recorded": stats["turn_count"],
        "total_session_cost_usd": stats["total_cost_usd"]
    }


def main():
    """Runs the MCP server over stdio."""
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
