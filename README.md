# Discord Helper Bot

A small Discord bot built with `discord.py` that supports slash commands for programming jokes, crypto prices, and reminders.

## Features

- `/joke` fetches a programming joke from JokeAPI and falls back to a local joke list if the API is unavailable.
- `/price` gets the current USD price for supported coins from CoinGecko.
- `/remind` stores reminders in SQLite and delivers them back into the channel when they are due.

## Requirements

- Python 3.11+
- A Discord application with a bot token

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_bot_token_here
REMINDER_DB_PATH=reminders.db
```

`REMINDER_DB_PATH` is optional. If omitted, the bot uses `reminders.db` in the project root.

## Run

```bash
python -m src.main
```

On startup, the bot:

- initializes the reminder database
- registers slash commands
- starts a background loop that checks for due reminders every 5 seconds

## Commands

- `/joke`
  Returns a random programming joke.
- `/price coin:<name>`
  Supported inputs include `bitcoin`, `btc`, `ethereum`, `eth`, `dogecoin`, `doge`, `solana`, and `sol`.
- `/remind message:<text> minutes:<number>`
  Stores a reminder and posts it in the same channel when the time is up.

## Project Structure

```text
src/
  bot.py                  Bot setup and background reminder loop
  main.py                 Application entry point
  config.py               Environment variable loading
  commands/               Slash command handlers
  services/               API and business logic
  storage/                SQLite persistence layer
```

## Notes

- The bot uses slash commands, so command registration can take a moment after startup.
- Joke and price commands depend on external APIs.
- Reminders are persisted in SQLite, so they survive bot restarts as long as the database file is kept.

Phase 1 Acceptance Criteria

- [X] bot works in a Discord server
- [X] all 3 commands work
- [X] repo is clean and documented
- [X] bot deployed online (Render/Railway)

Phase 2 Acceptance Criteria

- [X] allow joke category selection
- [X] return two part jokes with a delay between the parts