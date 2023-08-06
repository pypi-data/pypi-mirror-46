from enum import Enum
from datetime import time


class TimePrecision(Enum):
    hour = 1
    minute = 2
    second = 3
    millisecond = 4
    microsecond = 5


def time_to_seconds(a: time):
    """Gets the total seconds from a time object, discarding its microseconds information."""
    return a.hour * 60 * 60 + \
           a.minute * 60 + \
           a.second


def time_from_seconds(s: int):
    """Creates a new time object from seconds."""
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return time(int(h), int(m), int(s))


def time_to_microseconds(a: time):
    """Gets the total microseconds from a time object."""
    b = 1e6
    return a.hour * 60 * 60 * b + \
           a.minute * 60 * b + \
           a.second * b + \
           a.microsecond


def time_from_microseconds(a: int):
    """Creates a new time object from microseconds."""
    s, x = divmod(a, 1000000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return time(int(h), int(m), int(s), int(x))


def get_time_precision(*args):
    """
    Returns the minimum TimePrecision that can be used to represent times.

    :param args: any number of time compatible objects
    :return: the laziest precision at which time objects can be represented
    """
    if any(o.microsecond > 0 for o in args):
        return TimePrecision.microsecond

    if any(o.second > 0 for o in args):
        return TimePrecision.second

    if any(o.minute > 0 for o in args):
        return TimePrecision.minute

    return TimePrecision.hour

