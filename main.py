from telethon import TelegramClient, events, sync
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest

from functools import partial
import datetime as dt
import schedule
import json
import time
import pytz

import clocks


def update(client, bio):
    try:
        now = dt.datetime.now(TIMEZONE)
        clock = clocks.get_emoji(now)
        client(
            UpdateProfileRequest(
                about=bio + TIME_FORMAT.format(hour=now.hour, minute=now.minute, clock=clock)
            )
        )

    except Exception as error:
        phrase = type(error).__name__ + ': ' + error
        client.send_message('me', f'TimeSelfBot \n{phrase}')
        print(phrase)


def pend(account):
    client = TelegramClient(
        api_id=account['api-id'],
        api_hash=account['api-hash'],
        session=account['session']
    )
    client.start()
    client.send_message('me', 'TimeSelfBot started!')

    me = client(GetFullUserRequest('me'))
    updater = partial(update, client, me.full_user.about)
    updater()
    schedule.every().minute.at(':00').do(updater)


TIMEZONE_NAME = 'Asia/Tehran'
TIMEZONE = pytz.timezone(TIMEZONE_NAME)
TIME_FORMAT = "   Time: {hour}:{minute} {clock}"


if __name__ == '__main__':
    with open('accounts.json') as file:
        accounts = json.load(file)

    for name, info in accounts.items():
        pend(info)

    while True:
        schedule.run_pending()
        time.sleep(1)
