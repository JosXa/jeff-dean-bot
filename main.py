__version__ = "1.0.0"
import random
from uuid import uuid4

from decouple import config
from logzero import logger as log
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode, \
    ReplyKeyboardRemove
from telegram.ext import CommandHandler, InlineQueryHandler, Updater

from util import levenshteinDistance as distance


class Facts(object):
    def __init__(self):
        self.facts = []
        self.load_facts()

    def load_facts(self):
        with open("facts.txt", mode="r") as f:
            fact_lines = f.readlines()
        for fact in fact_lines:
            self.facts += [fact]

    def get_facts(self):
        return self.facts


all_facts = Facts()


def error(bot, update, error):
    log.error('Update "%s" caused error "%s"' % (update, error))


def send_help(bot, update):
    chat_id = update.message.chat_id
    log.info("Sending help...")
    bot.sendMessage(
        chat_id,
        "Get the hottest Jeff Dean fact delivered right to your inbox with /fact!\n\n"
        "Found more facts? Add them "
        "[here](https://github.com/JosXa/jeff-dean-bot/blob/master/facts.txt)!",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove()
    )


def get_random_fact():
    return random.choice(all_facts.get_facts())


def send_fact(bot, update):
    chat_id = update.message.chat_id
    fact = get_random_fact()
    log.info("Sending fact to " + str(chat_id) + ": " + fact)
    bot.sendMessage(chat_id, fact)


def inlinequery(bot, update):
    log.info("Answering inline query")
    query = update.inline_query.query
    results_list = []

    facts = all_facts.get_facts()
    search_results = [
        f
        for f in facts
        if distance(query, f, ignore_case=True) < 3 or query.lower() in f.lower()
    ]

    if search_results:
        facts = search_results[0:49]
    else:
        # 50 random facts
        range_start = random.randint(0, len(facts))
        facts = facts[range_start : range_start + 49]
        results_list.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title="No search results for '{}'.".format(query),
                input_message_content=InputTextMessageContent(
                    message_text=get_random_fact()
                ),
                description="Use a random fact below",
            )
        )

    for fact in facts:
        results_list.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title="Jeff Dean Fact",
                input_message_content=InputTextMessageContent(message_text=fact),
                description=fact,
            )
        )

    bot.answerInlineQuery(update.inline_query.id, results=results_list)


def main():
    bot_token = config("BOT_TOKEN")
    updater = Updater(bot_token)
    dp = updater.dispatcher
    dp.add_handler(InlineQueryHandler(inlinequery))

    # Commands
    dp.add_handler(CommandHandler("fact", send_fact))
    dp.add_handler(CommandHandler("start", send_help))
    dp.add_handler(CommandHandler("help", send_help))

    dp.add_error_handler(error)

    if not config("DEV", cast=bool, default=True):
        port = config("PORT", cast=int)
        updater.start_webhook(listen='0.0.0.0',
                              port=port,
                              url_path=bot_token)
        path = config("HOST") + bot_token
        log.info(f"Listening on '{path}'.")
        updater.bot.set_webhook(path)
    else:
        updater.start_polling()

    log.info("Listening...")

    updater.idle()


if __name__ == "__main__":
    main()
