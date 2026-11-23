"""
NexusPilot Cortex - Tool Output Compactor (Adaptive Context Compression)
Compresses terminal logs, diffs, JSON, and stack traces to preserve context window.
"""

import re
from typing import Dict, Any, Tuple


def collapse_repeated_lines(text: str) -> str:
    """Collapses consecutive identical or near-identical log lines."""
    lines = text.splitlines()
    if len(lines) < 4:
        return text

    collapsed = []
    prev_line = None
    repeat_count = 0

    for line in lines:
        stripped = line.strip()
        if stripped and stripped == prev_line:
            repeat_count += 1
        else:
            if repeat_count > 1:
                collapsed.append(f"  ... [repeated {repeat_count} times] ...")
            collapsed.append(line)
            prev_line = stripped
            repeat_count = 0

    if repeat_count > 1:
        collapsed.append(f"  ... [repeated {repeat_count} times] ...")

    return "\n".join(collapsed)


def fold_stack_traces(text: str) -> str:
    """
    Folds external vendor/framework stack trace frames (e.g., node_modules,
    site-packages, internal runtime) while keeping workspace app frames.
    """
    lines = text.splitlines()
    folded = []
    vendor_fold_count = 0

    vendor_patterns = [
        r"node_modules",
        r"site-packages",
        r"node:internal",
        r"internal/process",
        r"internal/modules",
        r"/lib/python[0-9]\.[0-9]+/",
        r"\\Python[0-9]+\\lib\\",
    ]

    for line in lines:
        is_vendor = any(re.search(pat, line, re.IGNORECASE) for pat in vendor_patterns)
        if is_vendor:
            vendor_fold_count += 1
        else:
            if vendor_fold_count > 0:
                folded.append(f"    ... [{vendor_fold_count} framework/vendor stack frames hidden] ...")
                vendor_fold_count = 0
            folded.append(line)

    if vendor_fold_count > 0:
        folded.append(f"    ... [{vendor_fold_count} framework/vendor stack frames hidden] ...")

    return "\n".join(folded)


def compact_diff(text: str) -> str:
    """Cleans up unified git diffs by stripping noisy metadata and empty hunks."""
    lines = text.splitlines()
    filtered = []
    for line in lines:
        # Skip index and git hash headers
        if line.startswith("index ") and ".." in line:
            continue
        if line.startswith("diff --git "):
            filtered.append(line)
            continue
        filtered.append(line)
    return "\n".join(filtered)


def compress_output(raw_text: str, max_chars: int = 5000) -> Tuple[str, Dict[str, Any]]:
    """
    Runs multi-stage output compression:
    1. Repeated log line collapse
    2. Framework stack frame folding
    3. Diff compaction
    4. Head/tail windowing if exceeding max_chars
    Returns (compressed_text, metrics_dict).
    """
    if not raw_text:
        return "", {"original_chars": 0, "compressed_chars": 0, "reduction_pct": 0.0}

    orig_len = len(raw_text)
    stage1 = collapse_repeated_lines(raw_text)
    stage2 = fold_stack_traces(stage1)
    stage3 = compact_diff(stage2)

    # If still exceeding max_chars, prioritize the tail (where exceptions, stack traces, and exit codes reside)
    final_text = stage3
    if len(final_text) > max_chars:
        # Give 30% to initialization header context, and 70% to terminal error diagnostics
        head_chars = int(max_chars * 0.30)
        tail_chars = max_chars - head_chars
        omitted = len(final_text) - (head_chars + tail_chars)
        final_text = (
            final_text[:head_chars]
            + f"\n\n... [NexusPilot Cortex: {omitted} characters omitted for context capacity] ...\n\n"
            + final_text[-tail_chars:]
        )

    compressed_len = len(final_text)
    reduction = ((orig_len - compressed_len) / orig_len * 100.0) if orig_len > 0 else 0.0

    return final_text, {
        "original_chars": orig_len,
        "compressed_chars": compressed_len,
        "reduction_pct": round(reduction, 1)
    }
