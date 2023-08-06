"""
Filter, segment and calculated fields operators related.
"""


class FilterOperators:
    """Filter operators"""
    IN_LIST = 'in_list'
    NOT_IN_LIST = 'not_in_list'
    STR_CONTAIN = 'str_contain'
    STR_NOT_CONTAIN = 'str_not_contain'
    STR_BEGIN_WITH = 'str_begin_with'
    STR_NOT_BEGIN_WITH = 'str_not_begin_with'
    STR_END_WITH = 'str_end_with'
    STR_NOT_END_WITH = 'str_not_end_with'
    REGEX_MATCH = 'regex_match'
    REGEX_NOT_MATCH = 'regex_not_match'
    EQUAL = 'equal'
    NOT_EQUAL = 'not_equal'
    DATE_EQUAL = 'date_equal'
    DATE_NOT_EQUAL = 'date_not_equal'
    IS_NULL = 'is_null'
    IS_NOT_NULL = 'is_not_null'
    GT = 'gt'
    GE = 'ge'
    LT = 'lt'
    LE = 'le'


class SegmentOperators(FilterOperators):
    """Segment operators"""


class CalculatedFieldOperators(FilterOperators):
    """Calculated fields operators"""
    