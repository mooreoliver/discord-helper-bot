from src.bot import HelperBot
from src.config import get_settings


def main() -> None:
    settings = get_settings()
    bot = HelperBot(reminder_db_path=settings.reminder_db_path)
    bot.run(settings.discord_token)


if __name__ == "__main__":
    main()