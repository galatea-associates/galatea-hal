import json
import logging

from gala_wit import GalaWit
from intenthandlers.utils import get_highest_confidence_entity
from intenthandlers.misc import say_quote
from intenthandlers.galastats import count_galateans
from slack_clients import is_direct_message


logger = logging.getLogger(__name__)

# this is a mapping of wit.ai intents to code that will handle those intents
intents = {
    'movie-quote': {'func': say_quote, 'sample': 'movie quote'},
    'galatean-count': {'func': count_galateans, 'sample': 'How many Galateans are in Boston?'},
    'randomize': {'func': randomize_options, 'sample': 'Decide between burgers and tacos'},
    'coin-flip': {'func': flip_coin, 'sample': 'flip a coin'}
}


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer
        self.wit_client = GalaWit()

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        # logger.info("event type is {}".format(event_type))
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.say_hi(event['channel'], event.get('user', ""))
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.say_hi(event['channel'], event.get('user', ""))
        else:
            pass


    def _handle_message(self, event):
        # Event won't have a user if slackbot is unfurling messages for you
        if 'user' not in event:
            return

        # Filter out messages from the bot itself
        if self.clients.is_message_from_me(event['user']):
            return

        msg_txt = event['text']
        channel_id = event['channel']

        # Filter out message unless this bot is mentioned or it is a direct message
        if not (is_direct_message(channel_id) or self.clients.is_bot_mention(msg_txt)):
            return

        # Remove mention of the bot so that the rest of the code doesn't need to
        msg_txt = self.clients.remove_mention(msg_txt).strip()

        # Ensure that we don't go to wit with messages posted by slackbot
        if event['user'] == "USLACKBOT":
            return

        # bot_uid = self.clients.bot_user_id()

        # Ask wit to interpret the text and send back a list of entities
        logger.info("Asking wit to interpret| {}".format(msg_txt))
        wit_resp = self.wit_client.interpret(msg_txt)

        # Find the intent with the highest confidence that met our default threshold
        intent_entity = get_highest_confidence_entity(wit_resp['entities'], 'intent')

        # If we couldn't find an intent entity, let the user know
        if intent_entity is None:
            self.msg_writer.write_prompt(channel_id, intents)
            return

        intent_value = intent_entity['value']
        if intent_value in intents:
            intents[intent_value]['func'](self.msg_writer, event, wit_resp['entities'])
        else:
            raise ReferenceError("No function found to handle intent {}".format(intent_value))



