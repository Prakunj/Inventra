# database/db.py

import sqlite3
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite database path
DB_PATH = BASE_DIR / "database" / "inventra.db"


def get_connection():
    """Return a SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn