import discord
from discord import app_commands

from src.services.joke_service import get_random_joke


def register(bot) -> None:
    @bot.tree.command(name="joke", description="Get a random programming joke")
    async def joke(interaction: discord.Interaction, category: str) -> None:
        await interaction.response.defer(thinking=True)

        result = await get_random_joke(category=category)
        await interaction.followup.send(result)
