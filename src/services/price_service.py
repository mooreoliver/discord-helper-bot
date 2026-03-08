import aiohttp

COIN_MAP = {
    "bitcoin": "bitcoin",
    "btc": "bitcoin",
    "ethereum": "ethereum",
    "eth": "ethereum",
    "dogecoin": "dogecoin",
    "doge": "dogecoin",
    "solana": "solana",
    "sol": "solana",
}


async def get_coin_price(query: str) -> str:
    normalized = query.strip().lower()
    coin_id = COIN_MAP.get(normalized)

    if not coin_id:
        supported = ", ".join(sorted(set(COIN_MAP.keys())))
        return f"Unknown coin: `{query}`. Try one of: {supported}"

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, timeout=10) as response:
            if response.status != 200:
                return "Price service is unavailable right now. Try again in a minute."

            data = await response.json()

    usd_price = data.get(coin_id, {}).get("usd")

    if usd_price is None:
        return f"Could not find a USD price for `{query}`."

    return f"{coin_id.title()}: ${usd_price:,.2f} USD"