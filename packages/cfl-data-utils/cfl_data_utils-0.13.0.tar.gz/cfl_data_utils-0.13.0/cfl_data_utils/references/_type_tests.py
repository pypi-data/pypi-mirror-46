"""The type tests are used in finding the type of a variable when it is a string, but could actually be of a different
type.

This can be commonly used when extracting data from a CSV.

Todo:
    * Could all potentially be replaced with single line ``isinstance`` statements or assertions
"""

from datetime import datetime


def int_type_test(value):
    """ Type test for potential integers

    Args:
        value: The value to be type tested
    """
    if isinstance(value, str):
        int(value)
    else:
        assert int(value) == value


def float_type_test(value):
    """ Type test for potential floats

    Args:
        value: The value to be type tested
    """
    if isinstance(value, str):
        float(value)
    else:
        assert float(value) == value


def datetime_type_test(value):
    """ Type test for potential datetimes

    Args:
        value: The value to be type tested
    """
    assert isinstance(value, datetime)
