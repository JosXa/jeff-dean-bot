import random
import re
import time
from pprint import pprint
from telepot import Bot


class JeffDeanBot(object):

    def __init__(self):
        self.load_facts()

    def load_facts(self):

        f = open('facts.txt', mode='r')
        fact_lines = f.readlines()
        f.close()

        # Speichere die gelesenen Facts in der self Variable
        self.facts = []
        for fact in fact_lines:
            self.facts += [fact]


    def sendFact(self, recipient):
        fact = random.choice(self.facts)
        print("Sending fact to " + str(recipient) + ": " + random.choice(self.facts))
        bot.sendMessage(str(recipient), fact)


    def handle_message(self, msg):
        # print("New message arrived: ")
        # pprint(msg)

        sender_id = msg['chat']['id']

        if 'text' in msg:
            text = msg['text']

            # Answer with fact
            if '/fact' in text:
                self.sendFact(sender_id)


jeffDeanBot = JeffDeanBot()

def handle(msg):
    jeffDeanBot.handle_message(msg)

bot = Bot('207013186:AAHaGrj8R9Ii8rVaUeS0JIWm5aKtY_BTU0U')
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(2) # ms
