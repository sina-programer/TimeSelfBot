from telethon import TelegramClient, events, sync
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest

from functools import partial
import datetime as dt
import schedule
import json
import time
import pytz


clocks = {
    0:  '🕛', 0.5:  '🕧',
    1:  '🕐', 1.5:  '🕜',
    2:  '🕑', 2.5:  '🕝',
    3:  '🕒', 3.5:  '🕞',
    4:  '🕓', 4.5:  '🕟',
    5:  '🕔', 5.5:  '🕠',
    6:  '🕕', 6.5:  '🕡',
    7:  '🕖', 7.5:  '🕢',
    8:  '🕗', 8.5:  '🕣',
    9:  '🕘', 9.5:  '🕤',
    10: '🕙', 10.5: '🕥',
    11: '🕚', 11.5: '🕦'
}


def get_clock_emoji(now):
    minute = now.minute
    hour = now.hour

    if minute >= 52:
        hour += 1

    elif minute >= 22:
        hour += .5

    return clocks[hour % 12]


def update(client, bio, time_fmt):
    try:
        now = dt.datetime.now(TIMEZONE)
        clock = get_clock_emoji(now)
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
