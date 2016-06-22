import logging
import random

logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {}'.format(msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message("{}".format(msg.encode('ascii', 'ignore')))

    def write_prompt(self, channel_id, handlers):
        bot_uid = self.clients.bot_user_id()
        txt = "Whut? I didn't quite understand that.  Here are some natural language *_intents_* I do understand:\n"
        for c in handlers:
            txt = txt + "> " + c + "\n"
        self.send_message(channel_id, txt)

#    def write_help(self,channel_id,intenthandlers):
#        bot_uid = self.clients.bot_user_id()
#        usage = "Hello Human!  I'll *_respond_* to the following intenthandlers in channel [" + channel_id + "]:\n"
#        for c in intenthandlers:
#            if c.allowed(channel_id):
#                usage = usage + "> " + c.usage(bot_uid) + "\n"
#
#        self.send_message(channel_id, usage)

    def say_hi(self, channel_id, user):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        if user != "":
            txt = '{}, <@{}>!'.format(random.choice(greetings), user)
        else:
            txt = '{}!'.format(random.choice(greetings))

        self.send_message(channel_id, txt)

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')
