#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
import ssl
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
from requests import Request, Session
s = Session()
import logging
import logging.handlers
LOG_FILENAME = '/tmp/telegram.log'
# create logger
logger = logging.getLogger("Telegram Logger")
logger.setLevel(logging.DEBUG)
# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1048576, backupCount=5)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter
handler.setFormatter(formatter)
# add ch to logger
logger.addHandler(handler)
#logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)
# Don't show logging messages while in production
#logging.disable(logging.DEBUG)
import sys
import inspect

# functions
def whoami():
    return inspect.stack()[1][3]


def send_message(token, params):
    """
    Use this method to send text messages.

    :param token: The API token generated following the instructions at https://core.telegram.org/bots#botfather
    :param params: A dictionary mapping the api method parameters to their arguments

    :type token: str
    :type params: dict

    :returns: On success, the sent Message is returned.
    :rtype: HTTP code

    """
    # required args
    logger.debug('received a call to %s', whoami())
    api_method = 'sendMessage'
    api_url_base = 'https://api.telegram.org/bot'

    get_url = '{base_url}{token}/{method}'.format(base_url=api_url_base, token=token, method=api_method)

    #print(get_url, params)
    logger.debug("%s %s", get_url, params)
    #s = Session()
    request = Request('POST', get_url, data=params).prepare()
    resp = s.send(request)
    logger.debug("%s", resp.status_code)
    return resp.status_code


def send_chat_action(token, params):
    """
    Use this method when you need to tell the user that something is happening on the bot's side. The status is set
    for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status).
    Example: The ImageBot needs some time to process a request and upload the image. Instead of sending a text message
    along the lines of “Retrieving image, please wait…”, the bot may use sendChatAction with action = upload_photo.
    The user will see a “sending photo” status for the bot.
    We only recommend using this method when a response from the bot will take a noticeable amount of time to arrive.

    :param chat_id: Unique identifier for the message recipient — User or GroupChat id
    :param action: Type of action to broadcast.  Choose one, depending on what the user is about to receive:
     typing for text messages, upload_photo for photos, record_video or upload_video for videos,
     record_audio or upload_audio for audio files, upload_document for general files,
     find_location for location data.
    :param token: The API token generated following the instructions at https://core.telegram.org/bots#botfather
    :param params: A dictionary mapping the api method parameters to their arguments

    :type chat_id: int
    :type action: ChatAction

    :returns: Returns True on success.
    :rtype: HTTP code

    """
    # required args
    #params = dict(chat_id=chat_id, action=action)

    logger.debug('received a call to %s', whoami())
    api_method = 'sendChatAction'
    api_url_base = 'https://api.telegram.org/bot'

    get_url = '{base_url}{token}/{method}'.format(base_url=api_url_base, token=token, method=api_method)

    #print(get_url, params)
    logger.debug("%s %s", get_url, params)
    #s = Session()
    request = Request('POST', get_url, data=params).prepare()
    resp = s.send(request)
    logger.debug("%s", resp.status_code)
    return resp.status_code


def get_me(token):
    """
    A simple method for testing your bot's auth token. Requires no parameters.
    Returns basic information about the bot in form of a User object.
    :param \*\*kwargs: Args that get passed down to :class:`TelegramBotRPCRequest`
    :returns: Returns basic information about the bot in form of a User object.
    :rtype: User
    """
    logger.debug('received a call to %s', whoami())
    api_method = 'getMe'
    api_url_base = 'https://api.telegram.org/bot'

    get_url = '{base_url}{token}/{method}'.format(base_url=api_url_base, token=token, method=api_method)

    #print(get_url, params)
    logger.debug("%s ", get_url)
    #s = Session()
    request = Request('POST', get_url).prepare()
    resp = s.send(request)
    logger.debug("%s %s", resp.status_code, resp.text)
    return resp.status_code


def parse_args():
    logger.debug('received a call to %s', whoami())
    parser = argparse.ArgumentParser(description='Nagios notification via Telegram')
    parser.add_argument('-t', '--token', nargs='?', required=True)
    parser.add_argument('-o', '--object_type', nargs='?', required=True)
    parser.add_argument('--contact', nargs='?', required=True)
    parser.add_argument('--notificationtype', nargs='?')
    parser.add_argument('--hoststate', nargs='?')
    parser.add_argument('--hostname', nargs='?')
    parser.add_argument('--hostaddress', nargs='?')
    parser.add_argument('--servicename', nargs='?')
    parser.add_argument('--servicestate', nargs='?')
    parser.add_argument('--servicedesc', nargs='?')
    parser.add_argument('--datetime', nargs='?')
    parser.add_argument('--output', nargs='?')
    args = parser.parse_args()
    return args


def send_notification(token, user_id, message):
    """
    Use this method to send notifications.

    :param token: The API token generated following the instructions at https://core.telegram.org/bots#botfather
    :param user_id: Unique identifier for the message recipient — User or GroupChat id
    :param message: Text of the message to be sent

    :type token: str
    :type user_id: int
    :type message: str

    :returns: On success, the sent Message is returned.
    :rtype: Message

    """
    logger.debug('received a call to %s', whoami())
    # required args
    params = dict(chat_id=user_id, text=message, parse_mode='Markdown')
    send_message(token, params)


def host_notification(args):
    logger.debug('received a call to %s', whoami())
    state = ''
    if args.hoststate == 'UP':
        state = u'\U00002705 '
    elif args.hoststate == 'DOWN':
        state = u'\U0001F525 '
    elif args.hoststate == 'UNREACHABLE':
        state = u'\U00002753 '

    return "%s* %s - %s is %s *\nNotification Type: %s\nHost: %s\nAddress: %s\nState: %s\n\nDate/Time: %s\nAdditional Info:\n`%s`\n" % (
        state,
        args.notificationtype,
        args.hostname.replace("_", "\_"),
        args.hoststate,
        args.notificationtype,
        args.hostname.replace("_", "\_"),
        args.hostaddress,
        args.hoststate,
        str(args.datetime).replace("+", " "),
        args.output
    )


def service_notification(args):
    logger.debug('received a call to %s', whoami())
    state = ''
    if args.servicestate == 'OK':
        state = u'\U00002705 '
    elif args.servicestate == 'WARNING':
        state = u'\U000026A0 '
    elif args.servicestate == 'CRITICAL':
        state = u'\U0001F525 '
    elif args.servicestate == 'UNKNOWN':
        state = u'\U00002753 '

    return "%s* %s - %s - %s is %s*\nNotification Type: %s\nService: %s\nHost: %s\nAddress: %s\nState: %s\n\nDate/Time: %s\nAdditional Info:\n`%s`\n" % (
        state,
        args.notificationtype,
        args.hostname.replace("_", "\_"),
        args.servicename.replace("_", "\_"),
        args.servicestate,
        args.notificationtype,
        args.servicedesc.replace("_", "\_"),
        args.hostname.replace("_", "\_"),
        args.hostaddress,
        args.servicestate,
        str(args.datetime).replace("+", " "),
        args.output
    )


def main():
    logger.debug('received a call to %s', whoami())
    logger.debug(sys.argv)
    args = parse_args()
    logger.debug(args)
    user_id = int(args.contact)
    get_me(args.token)
    #params = dict(chat_id=user_id, action='find_location')
    send_chat_action(args.token, dict(chat_id=user_id, action='find_location'))
    if args.object_type == 'host':
        message = host_notification(args)
    elif args.object_type == 'service':
        message = service_notification(args)
    send_notification(args.token, user_id, message)

if __name__ == '__main__':
    main()
