import random
import re
import time
from pprint import pprint
import telepot


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

            # Add a fact
            match = re.search(r'(/addfact)(.*)', text)
            if match is not None:
                fact = match.group(2) # Nur das Zitat, ohne /addfact
                fact = fact.replace('\n', '') # Zeilenumbrüche raus
                fact = fact.replace('\r', '') # Zeilenumbrüche raus
                fact = fact.strip() # Leerzeichen vorne und hinten raus
                if fact not in self.facts:
                    self.facts += [fact]
                    self.save_facts()
                    bot.sendMessage(str(sender_id), 'The fact has been added.')
                else:
                    bot.sendMessage(str(sender_id), 'This fact already exists.')


jeffDeanBot = JeffDeanBot()

def handle(msg):
    jeffDeanBot.handle_message(msg)

bot = telepot.Bot('207013186:AAHaGrj8R9Ii8rVaUeS0JIWm5aKtY_BTU0U')
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(2) # ms
