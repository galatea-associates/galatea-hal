import logging
import random

logger = logging.getLogger(__name__)


class Hi(object):
    def __init__(self):
        self.do_it = do_it


def do_it(msg_writer,event):
    greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
    if event.has_key('user'):
        txt = '{}, <@{}>!'.format(random.choice(greetings), event['user'])
    else:
        txt = '{}!'.format(random.choice(greetings))
        
    msg_writer.send_message(event['channel'], txt)

