import os
import sqlite3
import time
from typing import Dict, List, Optional

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
            # Create the table if it doesn't exist
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    state TEXT NOT NULL DEFAULT 'start',
                    car_data TEXT DEFAULT NULL
                )
            """
            )
            conn.commit()

            # Ensure columns exist (in case of schema upgrade)
            existing_columns = set(
                row[1] for row in cursor.execute("PRAGMA table_info(chat_history)")
            )
            if "state" not in existing_columns:
                cursor.execute(
                    "ALTER TABLE chat_history ADD COLUMN state TEXT NOT NULL DEFAULT 'start'"
                )
            if "car_data" not in existing_columns:
                cursor.execute(
                    "ALTER TABLE chat_history ADD COLUMN car_data TEXT DEFAULT NULL"
                )
            conn.commit()

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        state: str = "start",
        car_data: Optional[str] = None,
    ):
        ts = time.time()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chat_history (session_id, role, content, timestamp, state, car_data) 
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (session_id, role, content, ts, state, car_data),
            )
            conn.commit()

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT role, content, timestamp, state, car_data FROM chat_history 
                WHERE session_id = ? ORDER BY timestamp ASC
                """,
                (session_id,),
            )
            rows = cursor.fetchall()
            return [
                {
                    "role": role,
                    "content": content,
                    "timestamp": timestamp,
                    "state": state,
                    "car_data": car_data,
                }
                for role, content, timestamp, state, car_data in rows
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

    chat_manager = ChatHistoryManager(DB_PATH)

    # Example usage:
    # chat_manager.save_message("test_session_002", "user", "Do you have SUVs?", state="asking_car", car_data=None)

    history = chat_manager.get_history("test_session_001")
    pprint(history)

    chat_manager.delete_session("test_session_001")
