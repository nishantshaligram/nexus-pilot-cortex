"""
NexusPilot Cortex - Memory Store & Retrieval Engine
Handles semantic search, ranking, deduplication, and context injection generation.
"""

from typing import List, Dict, Any, Optional
import math
import time
import re
from .db import MemoryDatabase
from .extractor import extract_facts_from_text, generate_memory_id


class MemoryStore:
    def __init__(self, db: Optional[MemoryDatabase] = None):
        self.db = db or MemoryDatabase()

    def record_manual_fact(
        self,
        fact: str,
        subject: str = "custom",
        category: str = "preference",
        scope: str = "workspace",
        workspace_uri: Optional[str] = None,
        pinned: bool = False
    ) -> str:
        kw_tokens = re.findall(r"[a-zA-Z0-9]+", f"{subject} {fact}".replace("_", " ").lower())
        keywords = " ".join(set(kw_tokens))
        mem_id = generate_memory_id(subject, fact)
        
        return self.db.insert_or_update_memory(
            mem_id=mem_id,
            scope=scope,
            workspace_uri=workspace_uri,
            category=category,
            subject=subject,
            fact=fact,
            keywords=keywords,
            confidence=1.0,
            pinned=pinned
        )

    def auto_learn_from_interaction(
        self,
        user_input: str,
        scope: str = "workspace",
        workspace_uri: Optional[str] = None
    ) -> List[str]:
        candidates = extract_facts_from_text(user_input, scope=scope, workspace_uri=workspace_uri)
        saved_ids = []
        for c in candidates:
            m_id = self.db.insert_or_update_memory(
                mem_id=c["id"],
                scope=c["scope"],
                workspace_uri=c["workspace_uri"],
                category=c["category"],
                subject=c["subject"],
                fact=c["fact"],
                keywords=c["keywords"],
                confidence=c["confidence"],
                pinned=c["pinned"]
            )
            saved_ids.append(m_id)
        return saved_ids

    def search_relevant_memories(
        self,
        query: str,
        workspace_uri: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        all_memories = self.db.list_all(workspace_uri)
        if not all_memories or not query:
            return all_memories[:limit]

        query_tokens = set(re.findall(r"[a-zA-Z0-9]+", query.replace("_", " ").lower()))
        if not query_tokens:
            return all_memories[:limit]

        now = int(time.time())
        scored = []

        for m in all_memories:
            mem_keywords = set(m.get("keywords", "").replace("_", " ").split())
            fact_tokens = set(re.findall(r"[a-zA-Z0-9]+", f"{m.get('subject', '')} {m['fact']}".replace("_", " ").lower()))
            overlap = query_tokens.intersection(mem_keywords.union(fact_tokens))
            
            # Base match score
            match_score = len(overlap) * 2.0
            
            # Pinned items get high priority boost
            if m.get("pinned", 0):
                match_score += 5.0
            
            # Recency bonus (decaying over 30 days)
            age_days = (now - m.get("updated_at", now)) / 86400.0
            recency_multiplier = max(0.2, 1.0 - (age_days / 30.0))
            final_score = match_score * recency_multiplier

            if match_score > 0 or m.get("pinned", 0):
                scored.append((final_score, m))

        # Sort descending by score
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [item[1] for item in scored[:limit]]

        # Touch retrieved memories
        for r in results:
            self.db.touch_memory(r["id"])

        return results

    def generate_context_injection(
        self,
        query: str,
        workspace_uri: Optional[str] = None,
        limit: int = 4
    ) -> str:
        """
        Formats top relevant memories into a clean markdown block ready to be
        injected into active prompt context without blowing token budget.
        """
        memories = self.search_relevant_memories(query, workspace_uri=workspace_uri, limit=limit)
        if not memories:
            return ""

        lines = ["<!-- NexusPilot Cortex: Persistent Memories -->", "> [!NOTE] Recalled Project & User Memories:"]
        for m in memories:
            pin_badge = "📌 " if m.get("pinned") else "• "
            lines.append(f"> {pin_badge}**[{m['category'].upper()}]** {m['fact']}")

        return "\n".join(lines) + "\n"
