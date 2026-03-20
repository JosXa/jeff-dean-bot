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

By default it uses long polling. Set `TELEGRAM_MODE=webhook` plus
`WEBHOOK_PUBLIC_URL`, `WEBHOOK_PATH`, and `WEBHOOK_SECRET_TOKEN` to run it
behind a public HTTPS webhook endpoint.
