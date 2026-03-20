from __future__ import annotations

import logging
import os
import random
from typing import TYPE_CHECKING
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
)

from jeff_dean_bot.facts import fallback_facts, load_packaged_facts, random_fact, search_facts

if TYPE_CHECKING:
    from collections.abc import Sequence

LOGGER = logging.getLogger(__name__)

HELP_FACTS_URL = "https://github.com/JosXa/jeff-dean-bot/blob/master/src/jeff_dean_bot/facts.txt"
HELP_TEXT = (
    "Get the hottest Jeff Dean fact delivered right to your inbox with /fact!\n\n"
    f"Found more facts? Add them [here]({HELP_FACTS_URL})"
)


class JeffDeanBot:
    def __init__(self, facts: Sequence[str], *, rng: random.Random | None = None) -> None:
        self._facts = tuple(facts)
        self._rng = rng or random.Random()

    async def send_help(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        del context
        message = update.effective_message
        if message is None:
            return

        LOGGER.info("Sending help to chat %s", message.chat_id)
        await message.reply_text(
            HELP_TEXT,
            disable_web_page_preview=True,
            parse_mode=ParseMode.MARKDOWN,
        )

    async def send_fact(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        del context
        message = update.effective_message
        if message is None:
            return

        fact = random_fact(self._facts, rng=self._rng)
        LOGGER.info("Sending fact to chat %s", message.chat_id)
        await message.reply_text(fact)

    async def inline_query(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        del context
        inline_query = update.inline_query
        if inline_query is None:
            return

        query = inline_query.query.strip()
        results = search_facts(query, self._facts)
        articles: list[InlineQueryResultArticle] = []

        if not results:
            articles.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=f"No search results for '{query}'.",
                    input_message_content=InputTextMessageContent(
                        random_fact(self._facts, rng=self._rng)
                    ),
                    description="Use a random fact below",
                )
            )
            results = fallback_facts(self._facts, rng=self._rng)

        articles.extend(
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Jeff Dean Fact",
                input_message_content=InputTextMessageContent(fact),
                description=fact,
            )
            for fact in results
        )

        LOGGER.info("Answering inline query with %s results", len(articles))
        await inline_query.answer(articles, cache_time=0)

    def build_application(self, token: str) -> Application:
        application = ApplicationBuilder().token(token).build()
        application.add_handler(InlineQueryHandler(self.inline_query))
        application.add_handler(CommandHandler("fact", self.send_fact))
        application.add_handler(CommandHandler("start", self.send_help))
        application.add_handler(CommandHandler("help", self.send_help))
        application.add_error_handler(handle_error)
        return application


async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    LOGGER.exception("Unhandled update %r", update, exc_info=context.error)


def build_default_application() -> Application:
    token = os.environ["BOT_TOKEN"]
    facts = load_packaged_facts()
    return JeffDeanBot(facts).build_application(token)
