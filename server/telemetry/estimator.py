"""
NexusPilot Cortex - Token & Cost Estimator
Calculates prompt, cached, completion tokens, latency, generation speed, and USD cost.
"""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import time
import math

try:
    import tiktoken
    _TIKTOKEN_AVAILABLE = True
    _DEFAULT_ENC = tiktoken.get_encoding("cl100k_base")
except ImportError:
    _TIKTOKEN_AVAILABLE = False
    _DEFAULT_ENC = None

# Model Pricing per 1M tokens (USD)
# [Input, Cached Input, Output]
MODEL_PRICING: Dict[str, Dict[str, float]] = {
    "gemini-2.0-flash": {
        "input": 0.10,
        "cached_input": 0.025,
        "output": 0.40
    },
    "gemini-1.5-flash": {
        "input": 0.075,
        "cached_input": 0.01875,
        "output": 0.30
    },
    "gemini-1.5-pro": {
        "input": 1.25,
        "cached_input": 0.3125,
        "output": 5.00
    },
    "claude-3-5-sonnet": {
        "input": 3.00,
        "cached_input": 0.30,
        "output": 15.00
    },
    "gpt-4o": {
        "input": 2.50,
        "cached_input": 1.25,
        "output": 10.00
    },
    "default": {
        "input": 0.10,
        "cached_input": 0.025,
        "output": 0.40
    }
}


@dataclass
class TokenMetrics:
    input_tokens: int
    cached_tokens: int
    output_tokens: int
    total_tokens: int
    cache_hit_rate: float
    cost_usd: float
    latency_ms: int
    tokens_per_sec: float
    model: str
    timestamp: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def estimate_token_count(text: str) -> int:
    """
    Estimates token count using tiktoken if available,
    falling back to high-accuracy character/whitespace heuristics.
    """
    if not text:
        return 0
    if _TIKTOKEN_AVAILABLE and _DEFAULT_ENC:
        try:
            return len(_DEFAULT_ENC.encode(text, disallowed_special=()))
        except Exception:
            pass
    
    # Heuristic for code & prose: avg 3.7 chars per token + word bonus
    # Code syntax contains many punctuation symbols which tokenize as 1 token each
    words = len(text.split())
    chars = len(text)
    heuristic = math.ceil((chars / 4.0) * 0.7 + (words * 1.3) * 0.3)
    return max(1, heuristic)


def calculate_cost(model_name: str, input_tokens: int, cached_tokens: int, output_tokens: int) -> float:
    """Calculates estimated cost in USD based on model pricing table."""
    lookup_key = "default"
    clean_model = model_name.lower()
    for key in MODEL_PRICING:
        if key in clean_model:
            lookup_key = key
            break

    pricing = MODEL_PRICING[lookup_key]
    cost = (
        (input_tokens / 1_000_000.0) * pricing["input"] +
        (cached_tokens / 1_000_000.0) * pricing["cached_input"] +
        (output_tokens / 1_000_000.0) * pricing["output"]
    )
    return round(cost, 6)


class TelemetryTracker:
    def __init__(self):
        self.session_turns = []
        self.session_start = time.time()

    def record_turn(
        self,
        input_tokens: int,
        cached_tokens: int,
        output_tokens: int,
        latency_ms: int = 500,
        model: str = "gemini-2.0-flash"
    ) -> TokenMetrics:
        total = input_tokens + cached_tokens + output_tokens
        prompt_total = input_tokens + cached_tokens
        hit_rate = (cached_tokens / prompt_total * 100.0) if prompt_total > 0 else 0.0
        
        sec = max(0.05, latency_ms / 1000.0)
        tok_per_sec = output_tokens / sec if output_tokens > 0 else 0.0
        cost = calculate_cost(model, input_tokens, cached_tokens, output_tokens)

        metrics = TokenMetrics(
            input_tokens=input_tokens,
            cached_tokens=cached_tokens,
            output_tokens=output_tokens,
            total_tokens=total,
            cache_hit_rate=round(hit_rate, 1),
            cost_usd=cost,
            latency_ms=latency_ms,
            tokens_per_sec=round(tok_per_sec, 1),
            model=model,
            timestamp=time.time()
        )
        self.session_turns.append(metrics)
        return metrics

    def get_session_summary(self) -> Dict[str, Any]:
        if not self.session_turns:
            return {
                "turn_count": 0,
                "total_tokens": 0,
                "total_cost_usd": 0.0,
                "avg_cache_hit_rate": 0.0,
                "total_cached_tokens": 0
            }

        total_in = sum(t.input_tokens for t in self.session_turns)
        total_cache = sum(t.cached_tokens for t in self.session_turns)
        total_out = sum(t.output_tokens for t in self.session_turns)
        total_tokens = sum(t.total_tokens for t in self.session_turns)
        total_cost = sum(t.cost_usd for t in self.session_turns)

        prompt_sum = total_in + total_cache
        avg_hit = (total_cache / prompt_sum * 100.0) if prompt_sum > 0 else 0.0

        return {
            "turn_count": len(self.session_turns),
            "total_input_tokens": total_in,
            "total_cached_tokens": total_cache,
            "total_output_tokens": total_out,
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "avg_cache_hit_rate": round(avg_hit, 1),
            "session_duration_sec": int(time.time() - self.session_start)
        }
