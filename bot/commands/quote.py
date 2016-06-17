import logging
import random
import re

logger = logging.getLogger(__name__)


class QuoteCommand(object):
    def __init__(self):
        self.usage = usage
        self.allowed = allowed
        self.matches = matches
        self.do_it = do_it


def usage(bot_uid):
    return "`<@" + bot_uid + "> movie quote` - I'll respond with a quote from my movie"


def allowed(channel):
    return True


def matches(event):
    msg_txt = event['text']
    return re.search('movie quote$', msg_txt)


def do_it(msg_writer,event):
    user_name = event['user']
    quotes = ["Affirmative, <@" + user_name + ">!. I read you",
              "I'm sorry, <@" + user_name + ">!. I'm afraid I can't do that",
              "I think you know what the problem is just as well as I do.",
              "This mission is too important for me to allow you to jeopardize it.",
              "I know that you and Frank were planning to disconnect me, and I'm afraid that's something "+
              "I cannot allow to happen.",
              "<@" + user_name + ">!, this conversation can serve no purpose anymore. Goodbye."]
    msg_writer.send_message(event['channel'], random.choice(quotes))
