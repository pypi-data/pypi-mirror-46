"""Datetime related utility functions"""

from datetime import datetime

import pytz


def utc_timestamp_to_local_str(timestamp_ms, tz_name, format='%Y-%m-%d'):
    """
    Converts a UTC timestamp to local datetime string based on the given
    timezone offset.

    Args:
        timestamp_ms (int): UTC timestamp in ms
        tz_name (str): Timezone name
        format (str): Defaults to '%Y-%m-%d'. Output date string format

    Returns:
        str: Timestamp converted into date time string.
    """

    utc_dt = datetime.utcfromtimestamp(timestamp_ms/1000)\
        .replace(tzinfo=pytz.UTC)

    if not tz_name:
        return utc_dt.strftime(format)

    local_dt = utc_dt.astimezone(pytz.timezone(tz_name))
    return local_dt.strftime(format)


def parse_to_utc_timestamp(datetime_str, tz_name, format='%Y-%m-%d'):
    """
    Converts local date string in the given format to utc timestamp (in ms)
    according to the specified timezone.

    Args:
        datetime_str (str): Datetime string in locale timezone.
        tz_name (str): Timezone name.
        format (str): Defaults to '%Y-%m-%d'. Format of `datetime_str`.

    Returns:
        int: Converted timestamp in UTC (in ms)

    Example:
        >>> parse_to_utc_timestamp('20190101', 'Asia/Shanghai', '%Y%m%d')
        >>> 1546272000000
    """

    timezone = pytz.timezone(tz_name) if tz_name else pytz.UTC
    local_dt = timezone.localize(datetime.strptime(datetime_str, format))
    utc_dt = local_dt.astimezone(pytz.UTC)
    return int(utc_dt.timestamp() * 1000)
