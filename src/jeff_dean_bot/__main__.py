from __future__ import annotations

import logging

from jeff_dean_bot.bot import run_bot
from jeff_dean_bot.config import Settings


def main() -> int:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=logging.INFO,
    )
    settings = Settings.from_env()
    run_bot(settings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
