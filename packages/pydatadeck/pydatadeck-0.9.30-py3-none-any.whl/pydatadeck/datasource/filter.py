"""
Helpers for filtering data rows.
"""

import re
from functools import wraps

from .operators import FilterOperators

_filter_ops = {}

ONE_DAY_MILLISECOND = 86400000


def filter_op(operator):
    """
    Decorator factory for registering filter operator
    and its evaluation function.
    """

    def filter_op_decorator(func):
        assert operator not in _filter_ops
        _filter_ops[operator] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    return filter_op_decorator


@filter_op(FilterOperators.EQUAL)
def _equal(value, values):
    assert len(values) == 1
    return value == values[0]


@filter_op(FilterOperators.DATE_EQUAL)
def _date_equal(value, values):
    assert len(values) == 1
    start_val = values[0]
    end_val = start_val + ONE_DAY_MILLISECOND
    return start_val <= value < end_val


@filter_op(FilterOperators.DATE_NOT_EQUAL)
def _date_not_equal(value, values):
    return not _date_equal(value, values)


@filter_op(FilterOperators.NOT_EQUAL)
def _date_not_equal(value, values):
    return not _equal(value, values)


@filter_op(FilterOperators.IN_LIST)
def _in_list(value, values):
    return value in values


@filter_op(FilterOperators.NOT_IN_LIST)
def _not_in_list(value, values):
    return not _in_list(value, values)


@filter_op(FilterOperators.IS_NULL)
def _is_null(value, values): # pylint: disable=unused-argument
    return value is None


@filter_op(FilterOperators.IS_NOT_NULL)
def _is_not_null(value, values):
    return not _is_null(value, values)


@filter_op(FilterOperators.STR_CONTAIN)
def _str_contain(value, values):
    if not value:
        return False
    return any((v in value for v in values if v))


@filter_op(FilterOperators.STR_NOT_CONTAIN)
def _str_not_contain(value, values):
    if not value:
        return True
    return all((v not in value for v in values if v))


@filter_op(FilterOperators.STR_BEGIN_WITH)
def _str_begin_with(value, values):
    if not value:
        return False
    return any((value.startswith(v) for v in values if v))


@filter_op(FilterOperators.STR_NOT_BEGIN_WITH)
def _str_not_begin_with(value, values):
    if not value:
        return True
    return all((not value.startswith(v) for v in values if v))


@filter_op(FilterOperators.STR_END_WITH)
def _str_end_with(value, values):
    if not value:
        return False
    return any((value.endswith(v) for v in values if v))


@filter_op(FilterOperators.STR_NOT_END_WITH)
def _str_not_end_with(value, values):
    if not value:
        return True
    return all((not value.endswith(v) for v in values if v))


@filter_op(FilterOperators.REGEX_MATCH)
def _regex_match(value, values):
    if not value:
        return False
    return any((re.match(pattern, value) for pattern in values if pattern))


@filter_op(FilterOperators.REGEX_NOT_MATCH)
def _regex_not_match(value, values):
    if not value:
        return True
    return all((not re.match(pattern, value) for pattern in values if pattern))


@filter_op(FilterOperators.GT)
def _gt(value, values):
    assert len(values) == 1
    return value > values[0]


@filter_op(FilterOperators.GE)
def _ge(value, values):
    assert len(values) == 1
    return value >= values[0]


@filter_op(FilterOperators.LT)
def _lt(value, values):
    assert len(values) == 1
    return value < values[0]


@filter_op(FilterOperators.LE)
def _le(value, values):
    assert len(values) == 1
    return value <= values[0]


def _true(value, values): # pylint: disable=unused-argument
    return True


def _get_filter_funcs(filter_infos):
    return [(_filter_ops[f['operator']], f['values']) for f in filter_infos]


def filter(data_rows, field_ids, filters):

    """
    Filters the given data rows, and provides a generator yielding
    rows matching the given filters.

    Args:
        data_rows (list): data rows, each row is a list with values.
        field_ids (list): id of fields for each data column.
        filters (list): a list of FilterSegmentClause type, see
            https://app.swaggerhub.com/apis/Data83/datadeck-datasource-api/.

    Returns: generator of rows matching all the filters.
    """

    assert data_rows is not None
    assert field_ids is not None
    assert filters is not None

    filter_mapping = {}
    # One field could contain multiple AND filters.
    for f in filters:
        filter_mapping.setdefault(f['fieldId'], []).append(f)

    filter_funcs = [] # list of (filter_func, values) tuple
    for fid in field_ids:
        filter_infos = filter_mapping.get(fid)
        if filter_infos:
            filter_funcs.append(_get_filter_funcs(filter_infos))
        else:
            filter_funcs.append([(_true, [])])

    for row in data_rows:
        assert len(row) == len(field_ids)
        if all(func(value, values) for value, funcs in zip(row, filter_funcs)
               for (func, values) in funcs):
            yield row
