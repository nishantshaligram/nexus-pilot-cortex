"""
NexusPilot Cortex - Automated Test Suite
Validates Telemetry, Memory Engine, and Output Compactor.
"""

import os
import sys
import pytest

# Ensure server module is accessible
SERVER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "server"))
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

from telemetry import TelemetryTracker, render_badge, estimate_token_count, format_token_number
from memory import MemoryStore, MemoryDatabase, extract_facts_from_text
from compressor import compress_output, collapse_repeated_lines, fold_stack_traces, CacheAndContextAligner


def test_token_number_formatter():
    assert format_token_number(225) == "225"
    assert format_token_number(3100) == "3.1k"
    assert format_token_number(83700) == "83.7k"
    assert format_token_number(1250000) == "1.25M"


def test_telemetry_badge_formatting():
    tracker = TelemetryTracker()
    metrics = tracker.record_turn(
        input_tokens=3100,
        cached_tokens=83700,
        output_tokens=225,
        model="gemini-2.0-flash"
    )
    badge = render_badge(metrics, mode="compact")
    assert "Token Telemetry: In: 3.1k | Cache: 83.7k | Out: 225 | Total: 87.0k" in badge


def test_memory_crud_and_scoring(tmp_path):
    test_db = str(tmp_path / "test_memory.db")
    db = MemoryDatabase(test_db)
    store = MemoryStore(db)

    # 1. Manual insertion
    m_id = store.record_manual_fact(
        fact="Always use pnpm over npm",
        subject="package_manager",
        category="preference",
        pinned=True
    )
    assert m_id.startswith("mem_")

    # 2. Search
    results = store.search_relevant_memories("pnpm package manager")
    assert len(results) >= 1
    assert results[0]["pinned"] == 1
    assert "pnpm" in results[0]["fact"]

    # 3. Context Injection
    injection = store.generate_context_injection("pnpm")
    assert "Recalled Project & User Memories" in injection
    assert "Always use pnpm" in injection

    # 4. Deletion
    deleted = db.delete_memory(m_id)
    assert deleted is True


def test_autonomous_fact_extraction():
    sample = "Our database is PostgreSQL 16. Never use webpack in this project."
    facts = extract_facts_from_text(sample)
    assert len(facts) >= 2
    
    categories = {f["category"] for f in facts}
    assert "architecture" in categories
    assert "constraint" in categories


def test_output_compactor():
    noisy_text = (
        "Server starting...\n"
        + "Error: timeout\n" * 15
        + "  at node_modules/express/lib/router.js:45\n" * 5
        + "  at src/auth.ts:12\n"
    )
    compressed, metrics = compress_output(noisy_text, max_chars=300)
    assert metrics["reduction_pct"] > 30.0
    assert "repeated" in compressed or "framework" in compressed


def test_context_aligner():
    aligner = CacheAndContextAligner(context_limit=1_000_000, capacity_warning_pct=75.0)
    safe = aligner.check_budget(100_000)
    assert safe["status"] == "SAFE"

    warn = aligner.check_budget(800_000)
    assert warn["status"] == "WARNING"

    crit = aligner.check_budget(950_000)
    assert crit["status"] == "CRITICAL"
