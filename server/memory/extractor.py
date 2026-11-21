"""
NexusPilot Cortex - Autonomous Memory Extractor
Parses conversation turns to extract high-confidence facts, preferences, and constraints.
"""

import re
import hashlib
import time
from typing import List, Dict, Any, Optional

# Regex heuristic patterns for zero-shot fact extraction
EXTRACTION_PATTERNS = [
    # Explicit preferences ("always use pnpm", "never use yarn")
    (
        r"(?:always\s+use|prefer|from\s+now\s+on\s+use)\s+([a-zA-Z0-9_\-\.\s]+?)(?:\s+instead|\.|$)",
        "preference",
        "tool_preference",
        "User prefers using {match}"
    ),
    (
        r"(?:never\s+use|do\s+not\s+use|don't\s+use|avoid)\s+([a-zA-Z0-9_\-\.\s]+?)(?:\.|$)",
        "constraint",
        "prohibited_tool",
        "Do not use {match}"
    ),
    # Architecture and technical choices ("our database is Postgres", "backend runs on port 8080")
    (
        r"(?:our\s+database\s+is|db\s+is|using\s+database)\s+([a-zA-Z0-9_\-\.\s]+?)(?:\.|$)",
        "architecture",
        "database",
        "Project database: {match}"
    ),
    (
        r"(?:backend|server|app)\s+(?:runs\s+on|listens\s+on|port\s+is)\s+(?:port\s+)?([0-9]{2,5})",
        "architecture",
        "server_port",
        "Backend server port: {match}"
    ),
    (
        r"(?:project\s+is\s+written\s+in|using\s+framework|stack\s+is)\s+([a-zA-Z0-9_\-\.\s]+?)(?:\.|$)",
        "architecture",
        "tech_stack",
        "Project tech stack: {match}"
    ),
    # Direct user instruction to remember ("remember that ...", "keep in mind that ...")
    (
        r"(?:remember\s+that|please\s+remember|keep\s+in\s+mind\s+that)\s+([^\n\.]+)",
        "preference",
        "explicit_memory",
        "{match}"
    )
]


def generate_memory_id(subject: str, fact: str) -> str:
    raw = f"{subject}_{fact}_{time.time()}"
    digest = hashlib.sha256(raw.encode()).hexdigest()[:12]
    return f"mem_{digest}"


def extract_facts_from_text(
    text: str,
    scope: str = "workspace",
    workspace_uri: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Scans input text for learnable patterns.
    Returns list of candidate memory dictionaries.
    """
    results = []
    if not text:
        return results

    clean_text = text.strip()

    for pattern, category, subject, template in EXTRACTION_PATTERNS:
        matches = re.finditer(pattern, clean_text, re.IGNORECASE)
        for m in matches:
            val = m.group(1).strip()
            if len(val) < 2 or len(val) > 120:
                continue

            fact = template.format(match=val).strip()
            
            # Keywords generation: words from subject + val
            kw_tokens = re.findall(r"[a-zA-Z0-9_]+", f"{subject} {val}".lower())
            keywords = " ".join(set(kw_tokens))

            results.append({
                "id": generate_memory_id(subject, fact),
                "scope": scope,
                "workspace_uri": workspace_uri,
                "category": category,
                "subject": subject,
                "fact": fact,
                "keywords": keywords,
                "confidence": 0.90,
                "pinned": False
            })

    return results
