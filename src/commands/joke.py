import discord
from discord import app_commands

from src.services.joke_service import get_random_joke


def register(bot) -> None:
    @bot.tree.command(name="joke", description="Get a random programming joke")
    @app_commands.choices(joke_type=[app_commands.Choice(name="Single", value="single"), app_commands.Choice(name="Two-part", value="twopart")])
    async def joke(interaction: discord.Interaction, category: str, joke_type: app_commands.Choice[str]) -> None:
        await interaction.response.defer(thinking=True)

        result = await get_random_joke(category=category, joke_type=joke_type.value)
        await interaction.followup.send(result)
