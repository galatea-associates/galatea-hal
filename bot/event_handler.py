import json
import logging

from commands.hi import Hi
from commands.quote import Quote

logger = logging.getLogger(__name__)
commands = [Hi(), Quote()]


class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

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
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself
        # Event won't have a user if slackbot is unfurling messages for you
        if event.has_key('user') and not self.clients.is_message_from_me(event['user']):
            bot_uid = self.clients.bot_user_id()
            msg_txt = event['text']
            channel = event['channel']
            found_command = False
            usage = "Hello Human.  I'll *_respond_* to the following commands in channel ["+channel+"]:\n"
            if self.clients.is_bot_mention(msg_txt):
                for c in commands:
                    if c.allowed(channel):
                        usage = usage + "> " + c.usage(bot_uid) + "\n"
                        if c.matches(event):
                            found_command = True
                            c.do_it(self.msg_writer,event)
                            break

                if not found_command:
                    self.msg_writer.send_message(channel, usage)

