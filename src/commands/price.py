import discord
from discord import app_commands

from src.services.price_service import get_coin_price


def register(bot) -> None:
    @bot.tree.command(name="price", description="Get the current crypto price in USD")
    @app_commands.describe(coin="Crypto name or ticker, like bitcoin, btc, ethereum, or sol")
    async def price(interaction: discord.Interaction, coin: str) -> None:
        await interaction.response.defer(thinking=True)

        result = await get_coin_price(coin)
        await interaction.followup.send(result)