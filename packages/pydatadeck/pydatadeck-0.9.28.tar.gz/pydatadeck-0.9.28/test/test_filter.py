import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pydatadeck.datasource.filter import filter


def test_filter():

    rows = [
        [1, 'hello'],
        [2, None],
        [3, 'world']
    ]

    fids = ['f1', 'f2']

    r = filter(rows, fids, [
        {'fieldId': 'f3', 'operator': 'equal', 'values': [2]}])
    assert len(list(r)) == 3

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'equal', 'values': [2]}])
    assert len(list(r)) == 1

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'equal', 'values': [4]}])
    assert len(list(r)) == 0

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'not_equal', 'values': [2]}])
    assert len(list(r)) == 2

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'in_list', 'values': [0, 2]}])
    assert len(list(r)) == 1

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'in_list', 'values': [1, 2]}])
    assert len(list(r)) == 2

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'not_in_list', 'values': [2]}])
    assert len(list(r)) == 2

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'is_null', 'values': []}])
    assert len(list(r)) == 0

    r = filter(rows, fids, [
        {'fieldId': 'f2', 'operator': 'is_null', 'values': []}])
    assert len(list(r)) == 1

    r = filter(rows, fids, [
        {'fieldId': 'f2', 'operator': 'is_not_null', 'values': []}])
    assert len(list(r)) == 2

    r = filter(rows, fids, [
        {'fieldId': 'f2', 'operator': 'str_contain', 'values': ['el']}])
    assert len(list(r)) == 1

    r = filter(rows, fids, [
        {'fieldId': 'f2', 'operator': 'str_not_contain', 'values': ['el']}])
    assert len(list(r)) == 2

    r = filter(rows, fids, [
        {'fieldId': 'f2', 'operator': 'str_begin_with', 'values': ['he']}])
    assert len(list(r)) == 1

    r = filter(rows, fids, [
        {'fieldId': 'f2', 'operator': 'str_not_begin_with', 'values': ['he']}])
    assert len(list(r)) == 2

    r = filter(rows, fids, [
        {'fieldId': 'f2', 'operator': 'str_end_with', 'values': ['llo']}])
    assert len(list(r)) == 1

    r = filter(rows, fids, [
        {'fieldId': 'f2', 'operator': 'str_not_end_with', 'values': ['llo']}])
    assert len(list(r)) == 2

    r = filter(rows, fids, [
        {'fieldId': 'f2', 'operator': 'regex_match', 'values': ['.+ell.+']}])
    assert len(list(r)) == 1

    r = filter(rows, fids, [
        {'fieldId': 'f2', 'operator': 'regex_not_match', 'values': ['.+ell.+']}])
    assert len(list(r)) == 2

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'gt', 'values': [2]}])
    assert len(list(r)) == 1

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'ge', 'values': [2]}])
    assert len(list(r)) == 2

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'lt', 'values': [2]}])
    assert len(list(r)) == 1

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'ge', 'values': [2]}])
    assert len(list(r)) == 2

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'gt', 'values': [2]},
        {'fieldId': 'f2', 'operator': 'equal', 'values': ['world']}])
    assert len(list(r)) == 1

    r = filter(rows, fids, [
        {'fieldId': 'f1', 'operator': 'lt', 'values': [3]},
        {'fieldId': 'f1', 'operator': 'gt', 'values': [1]}])
    assert len(list(r)) == 1


def test_date_filter():
    rows = [
        [1, 1467849600000],  # 2016-07-07 08:00:00 +08:00
        [2, 1467936500000],  # 2016-07-08 08:08:20 +08:00
        [3, 1468022400000]   # 2016-07-09 08:00:00 +08:00
    ]
    fids = ['f1', 'f2']

    r = filter(rows, fids, [
        {'fieldId': 'f2', 'operator': 'date_equal', 'values': [1467936000000]}])
    assert len(list(r)) == 1

    r = filter(rows, fids, [
        {'fieldId': 'f2', 'operator': 'date_not_equal', 'values': [1467936000000]}])
    assert len(list(r)) == 2
