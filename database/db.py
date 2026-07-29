import sqlite3
import pandas as pd
from pathlib import Path
from contextlib import contextmanager

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite database path
DB_PATH = BASE_DIR / "database" / "inventra.db"


def get_connection():
    """Return a SQLite database connection with Row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class DBService:
    """Centralized Database Service to handle queries, connections, and Pandas integration."""

    @classmethod
    @contextmanager
    def get_cursor(cls):
        """Context manager that yields a database cursor and automatically handles commit/close."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            yield cursor, conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @classmethod
    def query(cls, sql: str, params: tuple = ()) -> list[dict]:
        """Execute a SELECT query and return all rows as a list of dictionaries."""
        with cls.get_cursor() as (cursor, _):
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]

    @classmethod
    def query_one(cls, sql: str, params: tuple = ()) -> dict | None:
        """Execute a SELECT query and return a single row as a dictionary or None."""
        with cls.get_cursor() as (cursor, _):
            cursor.execute(sql, params)
            row = cursor.fetchone()
            return dict(row) if row else None

    @classmethod
    def query_df(cls, sql: str, params: tuple = ()) -> pd.DataFrame:
        """Execute a SELECT query and return the result as a Pandas DataFrame."""
        conn = get_connection()
        try:
            df = pd.read_sql_query(sql, conn, params=params)
            return df
        finally:
            conn.close()

    @classmethod
    def execute(cls, sql: str, params: tuple = ()) -> int:
        """Execute an INSERT, UPDATE, or DELETE query and return lastrowid."""
        with cls.get_cursor() as (cursor, _):
            cursor.execute(sql, params)
            return cursor.lastrowid