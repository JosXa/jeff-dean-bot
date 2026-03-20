from __future__ import annotations

import random

from jeff_dean_bot.bot import HELP_FACTS_URL, HELP_TEXT, JeffDeanBot

FACTS = (
    "Jeff Dean proved that P=NP on a whiteboard.",
    "Jeff Dean warns compilers.",
)


def test_help_text_points_to_facts_file() -> None:
    assert f"[here]({HELP_FACTS_URL})" in HELP_TEXT


def test_bot_keeps_facts_for_runtime() -> None:
    bot = JeffDeanBot(FACTS, rng=random.Random(0))

    assert bot._facts == FACTS
