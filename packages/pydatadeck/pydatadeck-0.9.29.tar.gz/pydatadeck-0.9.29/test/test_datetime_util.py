from datetime import datetime
import pytz
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pydatadeck.datasource.datetime_util import *

TEST_TZ = 'Asia/Shanghai'
TEST_TIMEZONE = pytz.timezone(TEST_TZ)
TEST_FMT = '%Y-%m-%dT%H:%M:%S'


def test_utc_timestamp_to_local_str():
    utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    utc_now_ts = int(utc_now.timestamp() * 1000)

    r = utc_timestamp_to_local_str(utc_now_ts, TEST_TZ, TEST_FMT)
    assert r == utc_now.astimezone(TEST_TIMEZONE).strftime(TEST_FMT)

    r = utc_timestamp_to_local_str(utc_now_ts, None, TEST_FMT)
    assert r == utc_now.astimezone(pytz.UTC).strftime(TEST_FMT)


def test_utc_timestamp_to_local_str_dst():

    # before DST, US/Pacific is UTC-8
    utc_now = datetime(2019, 3, 1, 8, 0, 0, tzinfo=pytz.UTC)
    utc_now_ts = int(utc_now.timestamp() * 1000)

    r = utc_timestamp_to_local_str(utc_now_ts, 'US/Pacific', TEST_FMT)
    assert r == '2019-03-01T00:00:00'

    # after DST, US/Pacific is UTC-7
    utc_now = datetime(2019, 4, 1, 7, 0, 0, tzinfo=pytz.UTC)
    utc_now_ts = int(utc_now.timestamp() * 1000)

    r = utc_timestamp_to_local_str(utc_now_ts, 'US/Pacific', TEST_FMT)
    assert r == '2019-04-01T00:00:00'


def test_parse_to_utc_timestamp():
    s = '2019-05-02T13:48:01'
    dt = datetime.strptime(s, TEST_FMT)

    r = parse_to_utc_timestamp(s, TEST_TZ, TEST_FMT)
    assert r == int(TEST_TIMEZONE.localize(dt).astimezone(pytz.UTC).timestamp() * 1000)

    r = parse_to_utc_timestamp(s, None, TEST_FMT)
    assert r == int(dt.replace(tzinfo=pytz.UTC).timestamp() * 1000)


def test_parse_to_utc_timestamp_dst():

    # before DST, US/Pacific is UTC-8
    s = '2019-03-01T00:00:00'
    r = parse_to_utc_timestamp(s, 'US/Pacific', TEST_FMT)
    assert r == int(datetime(2019, 3, 1, 8, tzinfo=pytz.UTC).timestamp() * 1000)

    # after DST, US/Pacific is UTC-7
    s = '2019-04-01T00:00:00'
    r = parse_to_utc_timestamp(s, 'US/Pacific', TEST_FMT)
    assert r == int(datetime(2019, 4, 1, 7, tzinfo=pytz.UTC).timestamp() * 1000)
