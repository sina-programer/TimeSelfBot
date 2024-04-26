from telethon import TelegramClient, events, sync
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest

from functools import partial
from string import Template
import datetime as dt
import schedule
import json
import time
import pytz

import clocks


def rounded_time(datetime):
    if datetime.hour == datetime.minute:
        return True
    return False


def update(client, bio):
    try:
        now = dt.datetime.now(TIMEZONE)
        clock = clocks.get_emoji(now)
        client(
            UpdateProfileRequest(
                about=bio + TEMPLATE.substitute(
                    hour=now.hour,
                    minute=now.minute,
                    clock=clock,
                    suffix='🔥' if rounded_time(now) else ''
                )
            )
        )

    except Exception as error:
        phrase = type(error).__name__ + ': ' + str(error)
        client.send_message('me', f'TimeSelfBot \n{phrase}')
        print(phrase)


def pend(info):
    client = TelegramClient(
        api_id=info['api-id'],
        api_hash=info['api-hash'],
        session=info['session']
    )
    client.start()
    client.send_message('me', 'TimeSelfBot started!')

    me = client(GetFullUserRequest('me'))
    updater = partial(update, client, me.full_user.about)
    updater()
    schedule.every().minute.at(':00').do(updater)


TIMEZONE_NAME = 'Asia/Tehran'
TIMEZONE = pytz.timezone(TIMEZONE_NAME)
TEMPLATE = Template("  Time: $hour:$minute $clock $suffix")


if __name__ == '__main__':
    with open('accounts.json') as handler:
        accounts = json.load(handler)

    for account in accounts:
        pend(account)

    while True:
        schedule.run_pending()
        time.sleep(1)
