import random
import sys
import logging

from uuid import uuid4
from telegram import ParseMode, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, InlineQueryHandler

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

    def getFacts(self):
        return self.facts


all_facts = Facts()


def error(bot, update, error):
    logging.error('Update "%s" caused error "%s"' % (update, error))


def sendHelp(bot, update):
    chat_id = update.message.chat_id
    logging.info('Sending help...')
    bot.sendMessage(chat_id, 'Get the hottest Jeff Dean fact delivered right to your inbox with /fact!',
                    parse_mode=ParseMode.MARKDOWN)


def getRandomFact():
    return random.choice(all_facts.getFacts())


def sendFact(bot, update):
    chat_id = update.message.chat_id
    fact = getRandomFact()
    logging.info("Sending fact to " + str(chat_id) + ": " + fact)
    bot.sendMessage(chat_id, fact)


def inlinequery(bot, update):
    logging.info('Answering inline query')
    query = update.inline_query.query
    chat_id = update.inline_query.from_user.id
    results_list = list()

    facts = all_facts.getFacts()

    search_results = [f for f in facts if query.lower() in f.lower()]

    if len(search_results) > 0:
        facts = search_results
    else:
        # 50 random facts
        range_start = random.randint(0, len(facts))
        facts = facts[range_start:range_start + 50]

    for fact in facts:
        results_list.append(InlineQueryResultArticle(
            id=uuid4(),
            title='Your Jeff Dean Fact',
            input_message_content=InputTextMessageContent(message_text=fact),
            description=fact
        ))

    bot.answerInlineQuery(update.inline_query.id, results=results_list)


def main():
    """
    get token from command line args

    Usage:
    $ python3 bot.py [bot_token]
    """
    token = str(sys.argv[1])

    updater = Updater(token, workers=2)
    dp = updater.dispatcher
    dp.add_handler(InlineQueryHandler(inlinequery))

    # Commands
    dp.add_handler(CommandHandler("fact", sendFact))
    dp.add_handler(CommandHandler("help", sendHelp))

    dp.add_error_handler(error)
    updater.start_polling()

    print('Listening...')
    logging.info('Listening...')

    updater.idle()


if __name__ == '__main__':
    main()
