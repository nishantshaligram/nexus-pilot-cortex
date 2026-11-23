"""
Standard Library Test Runner for NexusPilot Cortex.
"""

import os
import sys
import tempfile
import unittest

# Add server directory
SERVER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "server"))
if SERVER_DIR not in sys.path:
    sys.path.insert(0, SERVER_DIR)

from telemetry import TelemetryTracker, render_badge, estimate_token_count, format_token_number
from memory import MemoryStore, MemoryDatabase, extract_facts_from_text
from compressor import compress_output, collapse_repeated_lines, fold_stack_traces, CacheAndContextAligner


class TestCortex(unittest.TestCase):
    def test_token_number_formatter(self):
        self.assertEqual(format_token_number(225), "225")
        self.assertEqual(format_token_number(3100), "3.1k")
        self.assertEqual(format_token_number(83700), "83.7k")
        self.assertEqual(format_token_number(1250000), "1.25M")

    def test_telemetry_badge_formatting(self):
        tracker = TelemetryTracker()
        metrics = tracker.record_turn(
            input_tokens=3100,
            cached_tokens=83700,
            output_tokens=225,
            model="gemini-2.0-flash"
        )
        badge = render_badge(metrics, mode="compact")
        self.assertIn("Token Telemetry: In: 3.1k | Cache: 83.7k | Out: 225 | Total: 87.0k", badge)

    def test_memory_crud_and_scoring(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            test_db = os.path.join(tmp_dir, "test_memory.db")
            db = MemoryDatabase(test_db)
            store = MemoryStore(db)

            m_id = store.record_manual_fact(
                fact="Always use pnpm over npm",
                subject="package_manager",
                category="preference",
                pinned=True
            )
            self.assertTrue(m_id.startswith("mem_"))

            results = store.search_relevant_memories("pnpm package manager")
            self.assertGreaterEqual(len(results), 1)
            self.assertEqual(results[0]["pinned"], 1)
            self.assertIn("pnpm", results[0]["fact"])

            injection = store.generate_context_injection("pnpm")
            self.assertIn("Recalled Project & User Memories", injection)
            self.assertIn("Always use pnpm", injection)

            deleted = db.delete_memory(m_id)
            self.assertTrue(deleted)

    def test_autonomous_fact_extraction(self):
        sample = "Our database is PostgreSQL 16. Never use webpack in this project."
        facts = extract_facts_from_text(sample)
        self.assertGreaterEqual(len(facts), 2)
        categories = {f["category"] for f in facts}
        self.assertIn("architecture", categories)
        self.assertIn("constraint", categories)

    def test_output_compactor(self):
        noisy_text = (
            "Server starting...\n"
            + "Error: timeout\n" * 15
            + "  at node_modules/express/lib/router.js:45\n" * 5
            + "  at src/auth.ts:12\n"
        )
        compressed, metrics = compress_output(noisy_text, max_chars=300)
        self.assertGreater(metrics["reduction_pct"], 30.0)

    def test_context_aligner(self):
        aligner = CacheAndContextAligner(context_limit=1_000_000, capacity_warning_pct=75.0)
        self.assertEqual(aligner.check_budget(100_000)["status"], "SAFE")
        self.assertEqual(aligner.check_budget(800_000)["status"], "WARNING")
        self.assertEqual(aligner.check_budget(950_000)["status"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()
