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


def update(client, bio, time_fmt):
    try:
        now = dt.datetime.now(TIMEZONE)
        clock = clocks.get_emoji(now)
        client(
            UpdateProfileRequest(
                about=bio + time_fmt.format(time=now.strftime('%H:%M'), clock=clock)
            )
        )

    except Exception as error:
        client.send_message('me', f'TimeSelfBot \nError: {error}')
        print(error)


def pend(account):
    client = TelegramClient(
        api_id=account['api-id'],
        api_hash=account['api-hash'],
        session=account['session']
    )
    client.start()
    client.send_message('me', 'TimeSelfBot started!')

    me = client(GetFullUserRequest('me'))
    updater = partial(update, client, me.full_user.about, '   Time: {time} {clock}')
    updater()
    schedule.every().minute.at(':00').do(updater)


TIMEZONE_NAME = 'Asia/Tehran'
TIMEZONE = pytz.timezone(TIMEZONE_NAME)


if __name__ == '__main__':
    with open('accounts.json') as file:
        accounts = json.load(file)

    for name, info in accounts.items():
        pend(info)

    while True:
        schedule.run_pending()
        time.sleep(1)
