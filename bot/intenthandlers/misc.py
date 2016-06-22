import logging
import random

logger = logging.getLogger(__name__)


def say_quote(msg_writer, event, wit_entities):
    user_name = event['user']
    quotes = ["Affirmative, <@" + user_name + ">!. I read you",
              "I'm sorry, <@" + user_name + ">!. I'm afraid I can't do that",
              "I think you know what the problem is just as well as I do.",
              "This mission is too important for me to allow you to jeopardize it.",
              "I know that you and Frank were planning to disconnect me, and I'm afraid that's something " +
              "I cannot allow to happen.",
              "<@" + user_name + ">!, this conversation can serve no purpose anymore. Goodbye."]
    msg_writer.send_message(event['channel'], "_{}_".format(random.choice(quotes)))
