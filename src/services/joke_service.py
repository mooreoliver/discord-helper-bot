import random

import aiohttp

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why did the developer go broke? Because he used up all his cache.",
    "There are 10 kinds of people in the world: those who understand binary and those who don't.",
    "Why do Java developers wear glasses? Because they don't C#.",
]

JOKESDOS = [
    [setup, delivery] for setup, delivery in [
        ("What are bits?", "Tiny things left when you drop your computer down the stairs."),
        ("What's yellow and can't swim?", "A bus full of children."),
        ("What's the object-oriented way to become wealthy?", "Inheritance."),
        ("What part of a vegetable are you not supposed to eat?", "The wheelchair.")
    ]
]   
def _get_fallback_for_type(joke_type: str) -> dict:
    if joke_type == "single":
        return {
            "type": "single",
            "joke": random.choice(JOKES)
        }
    elif joke_type == "twopart":
        setup, delivery = random.choice(JOKESDOS)
        return {
            "type": "twopart",
            "setup": setup,
            "delivery": delivery
        }

async def get_random_joke(category: str, joke_type: str = "single") -> dict:
    url = f"https://v2.jokeapi.dev/joke/{category}"
    params = {
        "safe-mode": "",
        "type": joke_type
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status != 200:
                    return _get_fallback_for_type(joke_type)

                data = await response.json()
                response_type = data.get("type")
    except (aiohttp.ClientError, TimeoutError):
        return _get_fallback_for_type(joke_type)

    if data.get("error"):
        return _get_fallback_for_type(joke_type)

    if response_type == "single":
        joke = data.get("joke")
        if joke:
            return {
                "type": "single",
                "joke": joke
            }
    if response_type == "twopart":
        setup = data.get("setup")
        delivery = data.get("delivery")
        if setup and delivery:
            return {
                "type": "twopart",
                "setup": setup,
                "delivery": delivery
            }

    return _get_fallback_for_type(joke_type)