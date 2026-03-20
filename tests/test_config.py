from __future__ import annotations

import os

import pytest

from jeff_dean_bot.config import Settings


@pytest.fixture(autouse=True)
def clear_runtime_env() -> None:
    for key in (
        "BOT_TOKEN",
        "TELEGRAM_MODE",
        "WEBHOOK_PUBLIC_URL",
        "WEBHOOK_PATH",
        "WEBHOOK_SECRET_TOKEN",
        "WEBHOOK_LISTEN",
        "WEBHOOK_PORT",
    ):
        os.environ.pop(key, None)


def test_settings_defaults_to_polling_mode() -> None:
    os.environ["BOT_TOKEN"] = "test-token"

    settings = Settings.from_env()

    assert settings.telegram_mode == "polling"
    assert settings.webhook is None


def test_settings_builds_webhook_configuration() -> None:
    os.environ["BOT_TOKEN"] = "test-token"
    os.environ["TELEGRAM_MODE"] = "webhook"
    os.environ["WEBHOOK_PUBLIC_URL"] = "https://jeff-dean-bot.josxa.dev/"
    os.environ["WEBHOOK_PATH"] = "telegram"
    os.environ["WEBHOOK_SECRET_TOKEN"] = "super-secret"
    os.environ["WEBHOOK_PORT"] = "8443"

    settings = Settings.from_env()

    assert settings.telegram_mode == "webhook"
    assert settings.webhook is not None
    assert settings.webhook.webhook_url == "https://jeff-dean-bot.josxa.dev/telegram"
    assert settings.webhook.url_path == "telegram"
    assert settings.webhook.port == 8443


def test_settings_rejects_non_https_webhook_url() -> None:
    os.environ["BOT_TOKEN"] = "test-token"
    os.environ["TELEGRAM_MODE"] = "webhook"
    os.environ["WEBHOOK_PUBLIC_URL"] = "http://jeff-dean-bot.josxa.dev"
    os.environ["WEBHOOK_SECRET_TOKEN"] = "super-secret"

    with pytest.raises(RuntimeError, match="https://"):
        Settings.from_env()
