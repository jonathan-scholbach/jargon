import typing as tp
import time


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
    diff = now-since_epoch

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
