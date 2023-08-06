"""
Aggregation related types and constants.
"""


class AggregationFunctions:
    """
    Aggregation functions.
    """
    SUM = 'sum'
    AVERAGE = 'average'
    MIN = 'min'
    MAX = 'max'
    STDEV = 'stdev'
    VAR = 'var'
    COUNTA = 'counta'
    DCOUNT = 'dcount'


class TimeGranularity:
    """
    Datetime aggregation granularities.
    """
    YEAR = 'year'
    QUARTER = 'quarter'
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    HOUR = 'hour'
    MINUTE = 'minute'
    SECOND = 'second'
    MILLISECOND = 'millisecond'
