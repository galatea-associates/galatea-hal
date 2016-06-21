import logging
import os
from wit import Wit

logger = logging.getLogger(__name__)


def merge(session_id, context, entities, msg):
    # Stub implementation
    return context


def say(self, session_id, context, msg):
    # Stub implementation
    raise RuntimeError("Should not have been called. Session: {}. Msg: {}. Context: {}".format(session_id,msg,context))


def error(self, session_id, context, e):
    # Stub implementation
    raise RuntimeError("Should not have been called. Session: {}. Err   : {}. Context: {}".format(session_id,str(e),
                                                                                                  context))


class GalaWit(object):
    def __init__(self):
        wit_token = os.getenv("WIT_ACCESS_TOKEN", "")
        logger.info("wit access token: {}".format(wit_token))

        if wit_token == "":
            logger.error("WIT_ACCESS_TOKEN env var not set.  Will not be able to connect to WIT.ai!")

        # Using dummy implementation of actions since we don't expect to use conversations for now
        # Simple "understanding" interactions with wit.ai shouldn't require these actions to be implemented
        self.actions = {
            'say': say,
            'error': error,
            'merge': merge,
        }

        self.wit_client = Wit(wit_token, self.actions, logger)

    def interpret(self,msg):
        resp = self.wit_client.message(msg)
        logger.info("resp {}".format(resp))
        return resp


