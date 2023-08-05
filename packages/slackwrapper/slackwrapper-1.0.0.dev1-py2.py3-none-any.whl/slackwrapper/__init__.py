import os

from slackclient import SlackClient

name = "slackwrapper"

__initialized = False


class MsgBlock():
    def __init__(self):
        self.block = []

    def add_text(self, text):
        section = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }
        self.block.append(section)

    def add_fields(self, fields: list) -> None:
        section = {
            "type": "section"}
        msg_fields = []
        for field in fields:
            msg_fields.append({"type": "mrkdwn", "text": field})
            if msg_fields.__len__() == 9:
                msg_fields.append({"type": "mrkdwn", "text": "*And some more...*\nBut it's limited to 10 fields."})
                break
        section["fields"] = msg_fields
        self.block.append(section)

    def add_context(self, text):
        section = {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": text
                }
            ]
        }
        self.block.append(section)

    def add_hr(self):
        section = {
            "type": "divider"
        }
        self.block.append(section)

    def get_block(self):
        return self.block


def create(icon: str, channel: str, user: str, token: str) -> None:
    global sc, ICON, CHANNEL, USER, __initialized
    proxy = {'https': os.environ.get('https_proxy') or None}
    sc = SlackClient(token, proxies=proxy)
    ICON = icon
    CHANNEL = channel
    USER = user
    __initialized = True


def __check_init():
    global __initialized
    if __initialized:
        pass
    else:
        raise Exception('Not initialized.')


def post_simple_text(text: str) -> str:
    global sc, ICON, CHANNEL, USER

    __check_init()

    res = sc.api_call(
        "chat.postMessage",
        channel=CHANNEL,
        username=USER,
        icon_emoji=ICON,
        text=text
    )
    return res['ts']


def post_block(block: MsgBlock) -> str:
    global sc, ICON, CHANNEL, USER

    __check_init()

    res = sc.api_call(
        "chat.postMessage",
        channel=CHANNEL,
        username=USER,
        icon_emoji=ICON,
        blocks=block.get_block()
    )
    return res['ts']


def post_simple_thread(text: str, thread: str) -> None:
    global sc, ICON, CHANNEL, USER

    __check_init()

    res = sc.api_call(
        "chat.postMessage",
        channel=CHANNEL,
        username=USER,
        icon_emoji=ICON,
        thread_ts=thread,
        text=text
    )
    return res['ts']


def edit_post(text: str, ts: str) -> None:
    global sc, ICON, CHANNEL, USER

    __check_init()

    res = sc.api_call(
        "chat.update",
        channel=CHANNEL,
        username=USER,
        icon_emoji=ICON,
        ts=ts,
        text=text
    )


def edit_post_block(block: MsgBlock, ts: str) -> None:
    global sc, ICON, CHANNEL, USER

    __check_init()

    res = sc.api_call(
        "chat.update",
        channel=CHANNEL,
        username=USER,
        icon_emoji=ICON,
        ts=ts,
        blocks=block.get_block()
    )


def delete_post(ts: str) -> None:
    global sc, CHANNEL

    __check_init()

    res = sc.api_call(
        "chat.delete",
        channel=CHANNEL,
        ts=ts
    )
