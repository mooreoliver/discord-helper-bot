import random

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why did the developer go broke? Because he used up all his cache.",
    "There are 10 kinds of people in the world: those who understand binary and those who don't.",
    "Why do Java developers wear glasses? Because they don't C#.",
]


def get_random_joke() -> str:
    return random.choice(JOKES)