import datetime
import time

import dateutil
import pytz
from croniter import croniter

EPOCH_START_DATETIME = datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)


def get_iso_format_utcnow():
    return datetime.datetime.utcnow().isoformat() + 'Z'


def to_epoch(dt):
    return (dt - EPOCH_START_DATETIME).total_seconds()


def iso_to_datetime(dt_string):
    return dateutil.parser.parse(dt_string)


def get_croniter(schedule):
    schedule = schedule.split()
    schedule.append(schedule.pop(0))
    return croniter(' '.join(schedule), time.time())
