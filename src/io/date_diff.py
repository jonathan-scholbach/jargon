import typing as tp
import time


from src.io import pluralize

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY
MONTH = 31 * DAY


def date_diff(since_epoch: tp.Optional[float]) -> str:
    if not since_epoch:
        return "never"

    now = time.time()
    diff = now - since_epoch

    if diff > MONTH:
        res = "> 1 month"
    elif diff > WEEK:
        res = pluralize(int(diff / WEEK), "week")
    elif diff > DAY:
        res = pluralize(int(diff / DAY), "day")
    elif diff > HOUR:
        res = pluralize(int(diff / HOUR), "hour")
    elif diff > MINUTE:
        res = pluralize(int(diff / MINUTE), "minute")
    else:
        res = "< 1 minute"

    return res + " ago"
