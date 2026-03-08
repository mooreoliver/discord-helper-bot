import aiosqlite


class ReminderStore:
    def __init__(self, db_path: str = "reminders.db") -> None:
        self.db_path = db_path

    async def initialize(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    channel_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    remind_at TEXT NOT NULL,
                    sent INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            await db.commit()

    async def add_reminder(
        self,
        user_id: int,
        channel_id: int,
        message: str,
        remind_at: str,
    ) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO reminders (user_id, channel_id, message, remind_at, sent)
                VALUES (?, ?, ?, ?, 0)
                """,
                (user_id, channel_id, message, remind_at),
            )
            await db.commit()

    async def get_due_reminders(self, now_iso: str) -> list[tuple]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                SELECT id, user_id, channel_id, message, remind_at
                FROM reminders
                WHERE sent = 0 AND remind_at <= ?
                """,
                (now_iso,),
            )
            rows = await cursor.fetchall()
            return rows

    async def mark_sent(self, reminder_id: int) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                UPDATE reminders
                SET sent = 1
                WHERE id = ?
                """,
                (reminder_id,),
            )
            await db.commit()