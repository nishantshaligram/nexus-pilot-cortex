"""
NexusPilot Cortex - Badge Formatter
Renders concise token telemetry badges in standard, detailed, and pill formats.
"""

from typing import Union
from .estimator import TokenMetrics


def format_token_number(n: int) -> str:
    """Formats an integer into a clean human-readable string (e.g., 3100 -> 3.1k)."""
    if n < 1000:
        return str(n)
    elif n < 100_000:
        val = n / 1000.0
        return f"{val:.1f}k"
    elif n < 1_000_000:
        return f"{round(n / 1000)}k"
    else:
        val = n / 1_000_000.0
        return f"{val:.2f}M"


def render_badge(metrics: TokenMetrics, mode: str = "compact") -> str:
    """
    Renders telemetry badge according to selected mode:
    - compact:  `Token Telemetry: In: 3.1k | Cache: 83.7k | Out: 225 | Total: 87.0k`
    - detailed: `📊 NexusPilot Telemetry | In: 3.1k | Cache: 83.7k (96.4% hit) | Out: 225 | Total: 87.0k | Cost: $0.0018`
    - pill:     `> ⚡ **Telemetry**: In: `3.1k` · Cache: `83.7k` · Out: `225` · Hit: `96%``
    - silent:   Returns empty string.
    """
    if mode == "silent":
        return ""

    in_str = format_token_number(metrics.input_tokens)
    cache_str = format_token_number(metrics.cached_tokens)
    out_str = format_token_number(metrics.output_tokens)
    total_str = format_token_number(metrics.total_tokens)

    if mode == "detailed":
        cost_str = f"${metrics.cost_usd:.4f}" if metrics.cost_usd >= 0.0001 else "<$0.0001"
        speed_str = f"{metrics.tokens_per_sec:.0f} tok/s"
        return (
            f"\n\n---\n"
            f"> 📊 **NexusPilot Telemetry** | In: {in_str} | Cache: {cache_str} ({metrics.cache_hit_rate}% hit) "
            f"| Out: {out_str} | Total: {total_str} | Speed: {speed_str} | Cost: {cost_str}"
        )

    if mode == "pill":
        return (
            f"\n\n---\n"
            f"> ⚡ **Token Telemetry**: In: `{in_str}` · Cache: `{cache_str}` ({metrics.cache_hit_rate}%) "
            f"· Out: `{out_str}` · Total: `{total_str}`"
        )

    # Standard / Compact mode (Exact user preference specification)
    return f"\n\nToken Telemetry: In: {in_str} | Cache: {cache_str} | Out: {out_str} | Total: {total_str}"
