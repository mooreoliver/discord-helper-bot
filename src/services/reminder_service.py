from datetime import datetime, timedelta, UTC

from src.storage.reminder_store import ReminderStore


class ReminderService:
    def __init__(self, store: ReminderStore) -> None:
        self.store = store

    async def create_reminder(
        self,
        user_id: int,
        channel_id: int,
        message: str,
        minutes: int,
    ) -> str:
        if minutes <= 0:
            raise ValueError("Minutes must be greater than 0.")

        remind_at = datetime.now(UTC) + timedelta(minutes=minutes)
        remind_at_iso = remind_at.isoformat()

        await self.store.add_reminder(
            user_id=user_id,
            channel_id=channel_id,
            message=message,
            remind_at=remind_at_iso,
        )

        return f"Okay — I’ll remind you in {minutes} minute(s)."

    async def get_due_reminders(self) -> list[tuple]:
        now_iso = datetime.now(UTC).isoformat()
        return await self.store.get_due_reminders(now_iso)

    async def mark_reminder_sent(self, reminder_id: int) -> None:
        await self.store.mark_sent(reminder_id)