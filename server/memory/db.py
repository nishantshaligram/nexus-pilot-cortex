"""
NexusPilot Cortex - Memory SQLite Database Manager
Provides local-first multi-tier memory storage with zero external dependencies.
"""

import sqlite3
import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

# Resilient local storage path resolution:
# 1. Environment variable CORTEX_DATA_DIR
# 2. Local plugin data dir (<plugin_root>/data)
# 3. User config dir (~/.gemini/config/plugins/nexus-pilot-cortex/data)
def get_default_data_dir() -> Path:
    env_dir = os.environ.get("CORTEX_DATA_DIR")
    if env_dir:
        p = Path(env_dir)
        p.mkdir(parents=True, exist_ok=True)
        return p

    # Local project data dir (always accessible without permission restrictions)
    local_data_dir = Path(__file__).resolve().parent.parent.parent / "data"
    try:
        local_data_dir.mkdir(parents=True, exist_ok=True)
        return local_data_dir
    except Exception:
        pass

    # Config dir fallback
    config_data_dir = Path(os.path.expanduser("~")) / ".gemini" / "config" / "plugins" / "nexus-pilot-cortex" / "data"
    try:
        config_data_dir.mkdir(parents=True, exist_ok=True)
        return config_data_dir
    except Exception:
        pass

    # Temporary directory fallback
    tmp_data_dir = Path(os.environ.get("TEMP", "/tmp")) / "nexus-pilot-cortex"
    tmp_data_dir.mkdir(parents=True, exist_ok=True)
    return tmp_data_dir

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS memories (
    id TEXT PRIMARY KEY,
    scope TEXT NOT NULL CHECK(scope IN ('global', 'workspace')),
    workspace_uri TEXT,
    category TEXT NOT NULL CHECK(category IN ('preference', 'architecture', 'episodic', 'constraint')),
    subject TEXT NOT NULL,
    fact TEXT NOT NULL,
    keywords TEXT,
    confidence REAL DEFAULT 1.0,
    pinned INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    access_count INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_memories_scope ON memories(scope, workspace_uri);
CREATE INDEX IF NOT EXISTS idx_memories_cat ON memories(category);
CREATE INDEX IF NOT EXISTS idx_memories_pinned ON memories(pinned);
"""


class MemoryDatabase:
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            data_dir = get_default_data_dir()
            self.db_path = str(data_dir / "cortex_memory.db")
        else:
            p = Path(db_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            self.db_path = str(p)
            
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.executescript(SCHEMA_SQL)
            conn.commit()

    def insert_or_update_memory(
        self,
        mem_id: str,
        scope: str,
        workspace_uri: Optional[str],
        category: str,
        subject: str,
        fact: str,
        keywords: str,
        confidence: float = 1.0,
        pinned: bool = False
    ) -> str:
        now = int(time.time())
        with self._get_connection() as conn:
            cur = conn.cursor()
            # If subject is a specific domain key (not generic), check for existing memory to update/supersede
            # For generic subjects, avoid accidental collisions and only update identical id or exact fact
            if subject and subject.lower() not in ("custom", "general", "explicit_memory", "user_fact"):
                cur.execute(
                    "SELECT id FROM memories WHERE scope = ? AND (workspace_uri = ? OR workspace_uri IS NULL) AND subject = ?",
                    (scope, workspace_uri, subject)
                )
            else:
                cur.execute(
                    "SELECT id FROM memories WHERE id = ? OR (scope = ? AND (workspace_uri = ? OR workspace_uri IS NULL) AND fact = ?)",
                    (mem_id, scope, workspace_uri, fact)
                )
            row = cur.fetchone()
            if row:
                existing_id = row["id"]
                cur.execute(
                    """
                    UPDATE memories 
                    SET fact = ?, keywords = ?, confidence = ?, pinned = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (fact, keywords, confidence, 1 if pinned else 0, now, existing_id)
                )
                conn.commit()
                return existing_id

            cur.execute(
                """
                INSERT INTO memories (
                    id, scope, workspace_uri, category, subject, fact, keywords, confidence, pinned, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (mem_id, scope, workspace_uri, category, subject, fact, keywords, confidence, 1 if pinned else 0, now, now)
            )
            conn.commit()
            return mem_id

    def list_all(self, workspace_uri: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            if workspace_uri:
                cur.execute(
                    "SELECT * FROM memories WHERE scope = 'global' OR workspace_uri = ? ORDER BY pinned DESC, updated_at DESC",
                    (workspace_uri,)
                )
            else:
                cur.execute("SELECT * FROM memories ORDER BY pinned DESC, updated_at DESC")
            return [dict(row) for row in cur.fetchall()]

    def delete_memory(self, memory_id: str) -> bool:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            conn.commit()
            return cur.rowcount > 0

    def touch_memory(self, memory_id: str):
        now = int(time.time())
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE memories SET access_count = access_count + 1, updated_at = ? WHERE id = ?",
                (now, memory_id)
            )
            conn.commit()
