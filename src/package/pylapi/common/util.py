# Utilities

from datetime import datetime
from dateutil import tz
from copy import deepcopy

from .config import *
from .error import *
from .logger_util import *


def datetime_now():
    return datetime.now(tz=tz.tzlocal())


def datetime_now_isoformat():
    return datetime.utcnow().isoformat(sep='T', timespec='milliseconds') + "Z"


def now_string():
    return datetime_now().strftime('%Y-%m-%d %H:%M:%S')


def parse_time(dtStr):
    try:
        ret = datetime.strptime(dtStr, '%m%d%Y%H%M%S')  # Parse to naive
        ret = ret.replace(tzinfo=tz.tzutc())  # Replace naive with UTC
        ret = ret.astimezone(tz=tz.tzlocal())  # Convert to local
    except ValueError:
        ret = None
    return ret


def timestamp_ms(dtObj):
    td = dtObj - datetime(1970, 1, 1).replace(tzinfo=tz.tzutc())
    return int(td.days*86400 + td.seconds)*1000 + round(td.microseconds / 1000)


def time_ms_to_s(tms):
    return round(tms / 1000)


def time_s_to_ms(ts):
    return ts * 1000


def time_m_to_s(ts):
    return ts * 60


def timestamp_s(dtObj):
    return time_ms_to_s(timestamp_ms(dtObj))


def timestamp_to_datetime_obj(ts):
    return datetime.fromtimestamp(ts)
