import discord
from discord import app_commands

from src.services.reminder_service import ReminderService


def register(bot, reminder_service: ReminderService) -> None:
    @bot.tree.command(name="remind", description="Set a reminder in minutes")
    @app_commands.describe(
        message="What should I remind you about?",
        minutes="How many minutes from now?"
    )
    async def remind(
        interaction: discord.Interaction,
        message: str,
        minutes: int,
    ) -> None:
        try:
            result = await reminder_service.create_reminder(
                user_id=interaction.user.id,
                channel_id=interaction.channel_id,
                message=message,
                minutes=minutes,
            )
            await interaction.response.send_message(result)
        except ValueError as error:
            await interaction.response.send_message(str(error), ephemeral=True)