import typing as tp
import time


SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
WEEK = 7 * DAY
MONTH = 31 * DAY


def __plural(count: int, dimension: str):
    return f"{count} {dimension}{'s' if count != 1 else ''}"


def date_diff(since_epoch: tp.Optional[float]) -> str:
    if not since_epoch:
        return "never"

    now = time.time()
    diff = now - since_epoch

    if diff > MONTH:
        res = "> 1 month"
    elif diff > WEEK:
        res = __plural(int(diff / WEEK), "week")
    elif diff > DAY:
        res = __plural(int(diff / DAY), "day")
    elif diff > HOUR:
        res = __plural(int(diff / HOUR), "hour")
    elif diff > MINUTE:
        res = __plural(int(diff / MINUTE), "minute")
    else:
        res = "< 1 minute"

    return res + " ago"
