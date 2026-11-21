# Copyright (c) 2026 Nagi(Nagisns)
# Licensed under the MIT License.
# See the LICENSE file for details.

import sqlite3
from pathlib import Path

DB_FILE: Path = Path(__file__).with_name("level.db")

class XpRepository:
    @staticmethod
    def _execute(sql: str, params: tuple[int, ...] = ()) -> None:
        conn = sqlite3.connect(DB_FILE)
        try:
            conn.execute(sql, params)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def create() -> None:
        XpRepository._execute(
            """
            CREATE TABLE IF NOT EXISTS guild_xp (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                xp INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (guild_id, user_id)
            )
            """
        )

    @staticmethod
    def add_xp(guild_id: int, user_id: int, xp: int) -> int:
        conn = sqlite3.connect(DB_FILE)
        try:
            row = conn.execute(
                """
                INSERT INTO guild_xp (guild_id, user_id, xp) VALUES (?, ?, ?)
                ON CONFLICT(guild_id, user_id)
                DO UPDATE SET xp = guild_xp.xp + excluded.xp
                RETURNING xp
                """,
                (guild_id, user_id, xp),
            ).fetchone()
            conn.commit()
            return row[0]
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def get_user_xp(guild_id: int, user_id: int) -> int | None:
        conn = sqlite3.connect(DB_FILE)
        try:
            row = conn.execute(
                "SELECT xp FROM guild_xp WHERE guild_id = ? AND user_id = ?",
                (guild_id, user_id),
            ).fetchone()
            if row is None:
                return None

            return row[0]
        finally:
            conn.close()
