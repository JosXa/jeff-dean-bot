# Jeff Dean Bot

Tiny Telegram bot that replies with random Jeff Dean facts.

## Development

```bash
uv sync
mise run check
uv run pytest
uv run jeff-dean-bot
```

The bot reads `BOT_TOKEN` from the environment.
