import os

__version__ = "1.0.0"
import logging
import random
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import CommandHandler, InlineQueryHandler, Updater

from util import levenshteinDistance as distance

logging.basicConfig(filename='bot.log', level=logging.INFO)


class Facts(object):
    def __init__(self):
        self.facts = []
        self.load_facts()

    def load_facts(self):
        f = open('facts.txt', mode='r')
        fact_lines = f.readlines()
        f.close()

        for fact in fact_lines:
            self.facts += [fact]

    def get_facts(self):
        return self.facts


all_facts = Facts()


def error(bot, update, error):
    logging.error('Update "%s" caused error "%s"' % (update, error))


def send_help(bot, update):
    chat_id = update.message.chat_id
    logging.info('Sending help...')
    bot.sendMessage(
        chat_id,
        'Get the hottest Jeff Dean fact delivered right to your inbox with /fact!',
        parse_mode=ParseMode.MARKDOWN)


def get_random_fact():
    return random.choice(all_facts.get_facts())


def send_fact(bot, update):
    chat_id = update.message.chat_id
    fact = get_random_fact()
    logging.info("Sending fact to " + str(chat_id) + ": " + fact)
    bot.sendMessage(chat_id, fact)


def inlinequery(bot, update):
    logging.info('Answering inline query')
    query = update.inline_query.query
    results_list = list()

    facts = all_facts.get_facts()
    search_results = [
        f for f in facts
        if distance(query, f, ignore_case=True) < 3 or query.lower() in f.lower()
    ]

    if len(search_results) > 0:
        facts = search_results[0:49]
    else:
        # 50 random facts
        range_start = random.randint(0, len(facts))
        facts = facts[range_start:range_start + 49]
        results_list.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title="No search results for '{}'.".format(query),
                input_message_content=InputTextMessageContent(
                    message_text=get_random_fact()),
                description='Use a random fact below'))

    for fact in facts:
        results_list.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title='Jeff Dean Fact',
                input_message_content=InputTextMessageContent(
                    message_text=fact),
                description=fact))

    bot.answerInlineQuery(update.inline_query.id, results=results_list)


def main():
    token = "207013186:AAGimWjXwN9PlvHIW_EWfOgbLAQ3SVIESik"

    updater = Updater(token, workers=2)
    dp = updater.dispatcher
    dp.add_handler(InlineQueryHandler(inlinequery))

    # Commands
    dp.add_handler(CommandHandler("fact", send_fact))
    dp.add_handler(CommandHandler("help", send_help))

    dp.add_error_handler(error)

    updater.start_webhook(
        listen='0.0.0.0',
        port=os.environ.get("DOKKU_PROXY_PORT"),
        url_path=token,
    )

    print('Listening...')
    logging.info('Listening...')

    updater.idle()


if __name__ == '__main__':
    main()
