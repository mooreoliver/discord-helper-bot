import discord
from discord.ext import commands, tasks

from src.commands import joke, price, remind
from src.services.reminder_service import ReminderService
from src.storage.reminder_store import ReminderStore


class HelperBot(commands.Bot):
    def __init__(self, reminder_db_path: str) -> None:
        intents = discord.Intents.default()

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

        self.reminder_store = ReminderStore(reminder_db_path)
        self.reminder_service = ReminderService(self.reminder_store)

    async def setup_hook(self) -> None:
        await self.reminder_store.initialize()

        joke.register(self)
        price.register(self)
        remind.register(self, self.reminder_service)

        self.check_reminders.start()

        synced = await self.tree.sync()
        print(f"Synced {len(synced)} command(s).")

    async def on_ready(self) -> None:
        if self.user is not None:
            print(f"Logged in as {self.user} (ID: {self.user.id})")

    @tasks.loop(seconds=5)
    async def check_reminders(self) -> None:
        due_reminders = await self.reminder_service.get_due_reminders()

        for reminder_id, user_id, channel_id, message, remind_at in due_reminders:
            channel = self.get_channel(channel_id)

            if channel is not None:
                await channel.send(f"<@{user_id}> Reminder: {message}")

            await self.reminder_service.mark_reminder_sent(reminder_id)

    @check_reminders.before_loop
    async def before_check_reminders(self) -> None:
        await self.wait_until_ready()