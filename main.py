from telethon import TelegramClient, events, sync
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest

import datetime as dt
import schedule
import time
import pytz

import meta

TEHRAN_TZ = pytz.timezone('Asia/Tehran')


def get_clock_emoji(now):
    hour = now.hour % 12
    minute = now.minute

    if minute >= 53:
        return meta.clocks[hour + 1]

    elif minute >= 23:
        return meta.clocks[hour + .5]

    return meta.clocks[hour]


def update(client, bio, time_fmt):
    try:
        now = dt.datetime.now(TEHRAN_TZ)
        clock = get_clock_emoji(now)
        client(
            UpdateProfileRequest(
                about=bio + time_fmt.format(time=now.strftime('%H:%M'), clock=clock)
            )
        )

    except Exception as error:
        print(error)


def pend(account):
    client = TelegramClient(
        api_id=account['api_id'],
        api_hash=account['api_hash'],
        session=account['session_name']
    )
    client.start()
    client.send_message('me', 'TimeSelfBot started!')

    me = client(GetFullUserRequest('me'))
    schedule.every().minute.do(lambda: update(client, me.full_user.about, '   Time: {time} {clock}'))



if __name__ == '__main__':
    for user, info in meta.accounts.items():
        pend(info)

    while True:
        schedule.run_pending()
        time.sleep(1)
