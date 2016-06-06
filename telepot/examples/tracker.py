import sys
import telepot
from telepot.delegate import per_from_id, create_open

"""
$ python3.4 tracker.py <token>

Tracks user actions across all flavors.
"""

class UserTracker(telepot.helper.UserHandler):
    def __init__(self, seed_tuple, timeout):
        super(UserTracker, self).__init__(seed_tuple, timeout)

        # keep track of how many messages of each flavor
        self._counts = {'chat': 0,
                        'inline_query': 0,
                        'chosen_inline_result': 0}

        self._answerer = telepot.helper.Answerer(self.bot)


    def on_message(self, msg):
        flavor = telepot.flavor(msg)
        self._counts[flavor] += 1

        # Display message counts separated by flavors
        print(self.id, ':',
              flavor, '+1', ':',
              ', '.join([str(self._counts[f]) for f in ['chat', 'inline_query', 'chosen_inline_result']]))

        # Have to answer inline query to receive chosen result
        if flavor == 'inline_query':
            def compute_answer():
                query_id, from_id, query_string = telepot.glance(msg, flavor=flavor)

                articles = [{'type': 'article',
                                 'id': 'abc', 'title': query_string, 'message_text': query_string}]

                return articles

            self._answerer.answer(msg, compute_answer)


TOKEN = sys.argv[1]

bot = telepot.DelegatorBot(TOKEN, [
    (per_from_id(), create_open(UserTracker, timeout=20)),
])
bot.message_loop(run_forever=True)
