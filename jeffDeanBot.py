import random
import sys

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler


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
    print('Update "%s" caused error "%s"' % (update, error))


def help(bot, update):
    chat_id = update.message.chat_id
    print('Sending help...')
    bot.sendMessage(chat_id, 'Get the hottest Jeff Dean fact delivered right to your inbox with /fact!',
                    parse_mode=ParseMode.MARKDOWN)


def sendFact(bot, update):
    chat_id = update.message.chat_id
    fact = random.choice(all_facts.getFacts())
    print("Sending fact to " + str(chat_id) + ": " + fact)
    bot.sendMessage(chat_id, fact)


def main():
    """
    get token from command line args

    Usage:
    $ python3 bot.py [bot_token]
    """
    token = str(sys.argv[1])

    updater = Updater(token, workers=10)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("fact", sendFact))
    dp.add_handler(CommandHandler("help", help))

    dp.add_error_handler(error)
    updater.start_polling()

    print('Listening...')

    updater.idle()


if __name__ == '__main__':
    main()
