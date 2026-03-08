import discord

from src.services.joke_service import get_random_joke


def register(bot) -> None:
    @bot.tree.command(name="joke", description="Get a random programming joke")
    async def joke(interaction: discord.Interaction) -> None:
        await interaction.response.send_message(get_random_joke())