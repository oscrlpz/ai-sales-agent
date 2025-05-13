import os
import sqlite3
import time
from typing import Dict, List

DB_PATH = "/home/oscar/projects/ai-sales-agent/data/db/chat_history.db"


class ChatHistoryManager:
    def __init__(self, db_path="chat_history.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(
            os.path.dirname(self.db_path), exist_ok=True
        ) if "/" in self.db_path else None
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp REAL NOT NULL
                )
            """
            )
            conn.commit()

    def save_message(self, session_id: str, role: str, content: str):
        ts = time.time()  # float timestamp (e.g. 1715609123.123)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chat_history (session_id, role, content, timestamp) 
                VALUES (?, ?, ?, ?)
            """,
                (session_id, role, content, ts),
            )
            conn.commit()

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT role, content, timestamp FROM chat_history 
                WHERE session_id = ? ORDER BY timestamp ASC
            """,
                (session_id,),
            )
            rows = cursor.fetchall()
            return [
                {"role": role, "content": content, "timestamp": timestamp}
                for role, content, timestamp in rows
            ]

    def delete_session(self, session_id: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM chat_history WHERE session_id = ?", (session_id,)
            )
            conn.commit()


if __name__ == "__main__":
    from pprint import pprint

    # Example usage
    chat_manager = ChatHistoryManager(DB_PATH)

    # # Save a message
    # chat_manager.save_message("test_session_001", "user", "Hello, how are you?")
    # chat_manager.save_message("test_session_001", "assistant", "I'm fine, thank you!")

    # Retrieve chat history
    history = chat_manager.get_history("test_session_001")
    pprint(history)

    # Delete session
    chat_manager.delete_session("test_session_001")
