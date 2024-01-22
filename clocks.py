import datetime as dt

clocks = {
    0:  '🕛', 
    0.5:  '🕧',
    1:  '🕐', 
    1.5:  '🕜',
    2:  '🕑', 
    2.5:  '🕝',
    3:  '🕒', 
    3.5:  '🕞',
    4:  '🕓', 
    4.5:  '🕟',
    5:  '🕔', 
    5.5:  '🕠',
    6:  '🕕', 
    6.5:  '🕡',
    7:  '🕖', 
    7.5:  '🕢',
    8:  '🕗', 
    8.5:  '🕣',
    9:  '🕘', 
    9.5:  '🕤',
    10: '🕙', 
    10.5: '🕥',
    11: '🕚', 
    11.5: '🕦'
}


def prepare_hour(hour, minute):
    if minute >= 52:
        return hour+1
    if minute >= 22:
        return hour+.5
    return hour


def get_emoji(datetime=None):
    if datetime is None:
        datetime = dt.datetime.now()
    hour = prepare_hour(datetime.hour, datetime.minute)
    return clocks[hour % 12]
