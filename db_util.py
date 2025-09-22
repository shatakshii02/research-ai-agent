import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DB_DIR, "reports.db")

def _ensure_db():
    os.makedirs(DB_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            summary TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)
        conn.commit()

def save_report(query: str, summary: str) -> int:
    _ensure_db()
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO reports (query, summary, created_at) VALUES (?, ?, ?)",
            (query, summary, datetime.utcnow().isoformat(timespec="seconds")+"Z")
        )
        conn.commit()
        return cur.lastrowid

def get_all_reports() -> List[Dict]:
    _ensure_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id, query, created_at FROM reports ORDER BY id DESC")
        rows = cur.fetchall()
        return [dict(r) for r in rows]

def get_report(report_id: int) -> Optional[Dict]:
    _ensure_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id, query, summary, created_at FROM reports WHERE id = ?", (report_id,))
        row = cur.fetchone()
        return dict(row) if row else None
