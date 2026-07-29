import json
from datetime import datetime
from database.db import DBService


class ChatService:
    """Service responsible for persisting and retrieving chat sessions and message history."""

    @staticmethod
    def create_session(session_id: str, title: str) -> dict:
        """Create a new chat session."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = """
            INSERT INTO chat_sessions (session_id, title, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """
        DBService.execute(sql, (session_id, title, now, now))
        return {
            "session_id": session_id,
            "title": title,
            "created_at": now,
            "updated_at": now,
            "messages": [],
        }

    @staticmethod
    def get_all_sessions() -> list[dict]:
        """Fetch all chat sessions ordered by updated_at DESC with message count."""
        sql = """
            SELECT s.session_id, s.title, s.created_at, s.updated_at,
                   COUNT(m.id) as message_count
            FROM chat_sessions s
            LEFT JOIN chat_messages m ON s.session_id = m.session_id
            GROUP BY s.session_id
            ORDER BY s.updated_at DESC
        """
        return DBService.query(sql)

    @staticmethod
    def get_session_messages(session_id: str) -> list[dict]:
        """Fetch all messages for a specific chat session."""
        sql = """
            SELECT role, content, state_json, timestamp
            FROM chat_messages
            WHERE session_id = ?
            ORDER BY id ASC
        """
        rows = DBService.query(sql, (session_id,))
        messages = []
        for r in rows:
            msg = {
                "role": r["role"],
                "content": r["content"],
                "ts": r["timestamp"],
            }
            if r["state_json"]:
                try:
                    msg["state"] = json.loads(r["state_json"])
                except Exception:
                    msg["state"] = {}
            messages.append(msg)
        return messages

    @staticmethod
    def add_message(session_id: str, role: str, content: str = "", state: dict | None = None, ts: str | None = None) -> int:
        """Add a message to a chat session and update the session timestamp."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp = ts or datetime.now().strftime("%H:%M")
        state_json = json.dumps(state) if state else None

        sql_msg = """
            INSERT INTO chat_messages (session_id, role, content, state_json, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """
        msg_id = DBService.execute(sql_msg, (session_id, role, content, state_json, timestamp))

        # Touch session updated_at
        DBService.execute("UPDATE chat_sessions SET updated_at = ? WHERE session_id = ?", (now, session_id))
        return msg_id

    @staticmethod
    def update_session_title(session_id: str, title: str):
        """Update session title (e.g. from first user prompt)."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "UPDATE chat_sessions SET title = ?, updated_at = ? WHERE session_id = ?"
        DBService.execute(sql, (title, now, session_id))

    @staticmethod
    def delete_session(session_id: str):
        """Delete a chat session and its message history."""
        DBService.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
        DBService.execute("DELETE FROM chat_sessions WHERE session_id = ?", (session_id,))
