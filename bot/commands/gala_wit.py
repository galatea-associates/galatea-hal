import logging
import random
import os
from wit import Wit
from quote import Quote
import time

logger = logging.getLogger(__name__)


def usage(bot_uid):
    return "Say something to me in natural language and I'll try to understand it"


def allowed(channel):
    return True


def merge(session_id, context, entities, msg):
    return context


def select_quote(session_id, context):
    user_name = context['_user']
    quotes = ["Affirmative, <@" + user_name + ">!. I read you",
              "I'm sorry, <@" + user_name + ">!. I'm afraid I can't do that",
              "I think you know what the problem is just as well as I do.",
              "This mission is too important for me to allow you to jeopardize it.",
              "I know that you and Frank were planning to disconnect me, and I'm afraid that's something " +
              "I cannot allow to happen.",
              "<@" + user_name + ">!, this conversation can serve no purpose anymore. Goodbye."]

    context['movie_quote']=random.choice(quotes)
    return context


class GalaWit(object):
    def __init__(self,msg_writer):
        self.usage = usage
        self.allowed = allowed
        self.msg_writer = msg_writer

        wit_token = os.getenv("WIT_ACCESS_TOKEN", "")
        logger.info("wit access token: {}".format(wit_token))

        if wit_token == "":
            logger.error("WIT_ACCESS_TOKEN env var not set.  Will not be able to connect to WIT.ai!")

        # Limiting this to the min actions required since we don't expect to use conversations for now
        self.actions = {
            'say': self._say,
            'error': self._error,
            'merge': merge,
            'movie-quote': Quote().do_it
        }

        self.wit_client = Wit(wit_token, self.actions, logger)

    def _say(self, session_id, context, msg):
        self.msg_writer.send_message(context['_channel'], msg)

    def _error(self, session_id, context, e):
        logger.error("Error in session {} context {}.  Err: {}".format(session_id, str(context), str(e)))
        self._say(session_id, context, str(e))

    def matches(self, event):
        resp = self.wit_client.message(event['text'])
        logger.info("resp {}".format(resp))

        if 'intent' in resp['entities']:
            logger.info("Found intent {}".format(resp['entities']['intent']))
            event['wit_resp'] = resp
            return True
        return False

    def do_it(self, msg_writer, event):
        # Take the first intent for now.  We probably want to look at confidence levels in the future
        intent = event['wit_resp']['entities']['intent'][0]
        intent_value = intent['value']
        confidence = intent['confidence']
        logger.info("Using first intent found {} with confidence {}".format(intent_value,confidence));

        if intent_value in self.actions:
            action = self.actions[intent_value]
            action(msg_writer,event)
        else:
            raise ReferenceError("No function found to handle intent {}".format(intent_value))

        # prefix with underscore since channel and user seem to create 500 errors from WIT
        # context = {
        #            "_channel": str(event['channel']),
        #    "_user": str(event['user'])
        # }
        # session_id = "{}-{}-{}".format(event['channel'],event['user'],time.time())
        # logger.info("Calling wit with session {}. Ctx: {}. Msg {}.".format(session_id,context,event['text']))
        # self.wit_client.run_actions(session_id, "tell me a movie quote", context)


