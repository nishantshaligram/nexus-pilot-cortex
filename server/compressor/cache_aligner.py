"""
NexusPilot Cortex - Gemini Prefix Cache & Headroom Aligner
Optimizes context ordering and monitors token headroom to avoid context cliffs.
"""

from typing import Dict, Any, List


class CacheAndHeadroomAligner:
    def __init__(self, context_limit: int = 1_000_000, headroom_warning_pct: float = 75.0):
        self.context_limit = context_limit
        self.headroom_warning_pct = headroom_warning_pct

    def check_headroom(self, current_tokens: int) -> Dict[str, Any]:
        """
        Evaluates remaining context headroom.
        Returns status ('SAFE', 'WARNING', 'CRITICAL') and recommended actions.
        """
        usage_pct = (current_tokens / self.context_limit) * 100.0 if self.context_limit > 0 else 0.0
        remaining = max(0, self.context_limit - current_tokens)

        if usage_pct >= 90.0:
            status = "CRITICAL"
            recommendation = "Immediate context compaction required. Squash resolved tool calls and summarize earlier turns."
        elif usage_pct >= self.headroom_warning_pct:
            status = "WARNING"
            recommendation = "Headroom threshold reached. Recommend collapsing older conversation turns."
        else:
            status = "SAFE"
            recommendation = "Headroom optimal. Prefix caching active."

        return {
            "current_tokens": current_tokens,
            "context_limit": self.context_limit,
            "remaining_tokens": remaining,
            "usage_pct": round(usage_pct, 1),
            "status": status,
            "recommendation": recommendation
        }

    def validate_prefix_ordering(self, context_blocks: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Validates that static blocks (system prompts, rules) appear before dynamic blocks
        (conversation history, tool outputs) to preserve prefix cache validity.
        """
        violations = []
        saw_dynamic = False

        for idx, block in enumerate(context_blocks):
            b_type = block.get("type", "dynamic")
            if b_type == "dynamic":
                saw_dynamic = True
            elif b_type == "static" and saw_dynamic:
                violations.append({
                    "index": idx,
                    "block_name": block.get("name", "unnamed_static"),
                    "issue": "Static block found after dynamic block; breaks prefix cache breakpoint."
                })

        return {
            "cache_aligned": len(violations) == 0,
            "violations": violations,
            "advice": "Move static rules and pinned system declarations to the front of prompt."
        }
