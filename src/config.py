from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    discord_token: str
    reminder_db_path: str


def get_settings() -> Settings:
    discord_token = os.getenv("DISCORD_TOKEN")
    if not discord_token:
        raise RuntimeError("Missing DISCORD_TOKEN in .env")

    reminder_db_path = os.getenv("REMINDER_DB_PATH", "reminders.db")

    return Settings(
        discord_token=discord_token,
        reminder_db_path=reminder_db_path,
    )