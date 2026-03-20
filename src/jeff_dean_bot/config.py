from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlsplit

TelegramMode = Literal["polling", "webhook"]


@dataclass(frozen=True, slots=True)
class WebhookSettings:
    public_url: str
    path: str
    secret_token: str
    listen: str
    port: int

    @property
    def webhook_url(self) -> str:
        return f"{self.public_url}{self.path}"

    @property
    def url_path(self) -> str:
        return self.path.removeprefix("/")


@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    telegram_mode: TelegramMode = "polling"
    webhook: WebhookSettings | None = None

    @classmethod
    def from_env(cls) -> Settings:
        bot_token = os.environ["BOT_TOKEN"]
        raw_mode = os.getenv("TELEGRAM_MODE", "polling").strip().casefold()
        if raw_mode not in {"polling", "webhook"}:
            msg = "TELEGRAM_MODE must be either 'polling' or 'webhook'."
            raise RuntimeError(msg)

        if raw_mode == "polling":
            return cls(bot_token=bot_token, telegram_mode="polling", webhook=None)

        public_url = os.getenv("WEBHOOK_PUBLIC_URL", "").strip().rstrip("/")
        if not public_url:
            msg = "WEBHOOK_PUBLIC_URL is required when TELEGRAM_MODE=webhook."
            raise RuntimeError(msg)
        if not public_url.startswith("https://"):
            msg = "WEBHOOK_PUBLIC_URL must start with https:// for Telegram webhooks."
            raise RuntimeError(msg)
        if urlsplit(public_url).path not in {"", "/"}:
            msg = "WEBHOOK_PUBLIC_URL must not contain a path; use WEBHOOK_PATH instead."
            raise RuntimeError(msg)

        path = os.getenv("WEBHOOK_PATH", "/telegram").strip() or "/telegram"
        if not path.startswith("/"):
            path = f"/{path}"

        secret_token = os.getenv("WEBHOOK_SECRET_TOKEN", "").strip()
        if not secret_token:
            msg = "WEBHOOK_SECRET_TOKEN is required when TELEGRAM_MODE=webhook."
            raise RuntimeError(msg)

        listen = os.getenv("WEBHOOK_LISTEN", "0.0.0.0").strip() or "0.0.0.0"
        port_text = os.getenv("WEBHOOK_PORT", "8080").strip() or "8080"
        try:
            port = int(port_text)
        except ValueError as exc:
            msg = "WEBHOOK_PORT must be an integer."
            raise RuntimeError(msg) from exc

        return cls(
            bot_token=bot_token,
            telegram_mode="webhook",
            webhook=WebhookSettings(
                public_url=public_url,
                path=path,
                secret_token=secret_token,
                listen=listen,
                port=port,
            ),
        )
