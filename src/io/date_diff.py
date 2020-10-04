import typing as tp
import datetime as dt


MONTH = 60 * 60 * 24 * 31
WEEK = 60 * 60 * 24 * 7
DAY = 60 * 60 * 24
HOUR = 60 * 60
MINUTE = 60


def date_diff(datetime: tp.Optional["dt.datetime"]) -> str:
    if not datetime:
        return "never"

    now = dt.datetime.now()
    diff = (now - datetime).total_seconds()

    if diff > MONTH:
        res = "> 1 month"
    elif diff > WEEK:
        res = str(int(diff / WEEK)) + " weeks"
    elif diff > DAY:
        res = str(int(diff / DAY)) + " days"
    elif diff > HOUR:
        res = str(int(diff / HOUR)) + " hours"
    elif diff > MINUTE:
        res = str(int(diff / MINUTE)) + " minutes"
    else:
        res = "< 1 minute"

    return res + " ago"
