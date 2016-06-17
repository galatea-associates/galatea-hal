import logging
import random
import re

logger = logging.getLogger(__name__)


class Hi(object):
    def __init__(self):
        self.usage = usage
        self.allowed = allowed
        self.matches = matches
        self.do_it = do_it


def usage(bot_uid):
    return "`hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user. :wave:"


def allowed(channel):
    return True


def matches(event):
    msg_txt = event['text']
    return re.search('hi|hey|hello|howdy', msg_txt)


def do_it(msg_writer,event):
    greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
    txt = '{}, <@{}>!'.format(random.choice(greetings), event['user'])
    msg_writer.send_message(event['channel'], txt)

