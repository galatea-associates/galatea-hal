import json
import logging
import re

from gala_wit import GalaWit
from intents.hi import Hi
from intents.quote import Quote

logger = logging.getLogger(__name__)

intents = {
    'movie-quote':Quote().do_it
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
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            Hi().do_it(self.msg_writer,event)
        elif event_type == 'group_joined':
            # you joined a private group
            Hi().do_it(self.msg_writer,event)
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself
        if self.clients.is_message_from_me(event['user']):
            return

        # Event won't have a user if slackbot is unfurling messages for you
        if 'user' not in event:
            return

        msg_txt = event['text']
        channel_id = event['channel']

        # Filter out message unless this bot is mentioned or it is a direct message
        if not (self.clients.is_direct_message(channel_id) or self.clients.is_bot_mention(msg_txt)):
            return

        bot_uid = self.clients.bot_user_id()

        # Ask wit to interpret the text and send back a list of entities
        logger.info("Asking wit to interpret| {}".format(msg_txt))
        resp = self.wit_client.interpret(msg_txt)

        # The "intent" entity sent back by wit should map to an action on our side
        if 'intent' not in resp['entities']:
            logger.info("Could not find an intent in the response: {}".format(resp))
            self.msg_writer.write_prompt(channel_id)
            return

        logger.info("Found intent(s) in response {}".format(resp['entities']['intent']))

        # Take the first intent for now.  We probably want to look at confidence levels in the future
        intent = resp['entities']['intent'][0]
        intent_value = intent['value']
        confidence = intent['confidence']
        logger.info("Using first intent found {} with confidence {}".format(intent_value, confidence));

        if intent_value in intents:
            intents[intent_value](self.msg_writer, event)
        else:
            raise ReferenceError("No function found to handle intent {}".format(intent_value))


