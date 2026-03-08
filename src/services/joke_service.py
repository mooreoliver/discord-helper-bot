import random

import aiohttp

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why did the developer go broke? Because he used up all his cache.",
    "There are 10 kinds of people in the world: those who understand binary and those who don't.",
    "Why do Java developers wear glasses? Because they don't C#.",
]


def _get_fallback_joke() -> str:
    return random.choice(JOKES)


async def get_random_joke(category: str, joke_type: str) -> str:
    url = f"https://v2.jokeapi.dev/joke/{category}"
    params = {
        "safe-mode": "",
        "type": joke_type
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status != 200:
                    return _get_fallback_joke()

                data = await response.json()
    except (aiohttp.ClientError, TimeoutError):
        return _get_fallback_joke()

    if data.get("error"):
        return _get_fallback_joke()

    joke_type = data.get("type")
    if joke_type == "single":
        joke = data.get("joke")
        return joke or _get_fallback_joke()

    if joke_type == "twopart":
        setup = data.get("setup")
        delivery = data.get("delivery")
        if setup and delivery:
            return f"{setup}\n{delivery}"

    return _get_fallback_joke()
