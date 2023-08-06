"""These constants are used often amongst many projects, so have been made importable to reduce error in mis-typing
and effort to add them to each project
"""

from ._type_tests import datetime, datetime_type_test, float_type_test, int_type_test

RESTART_OPTION = '[Restart]'
Q = 'question'
EXIT_OPTION = '[Exit]'
NEW_MONTH_FLAG = datetime.today().day == 1

TYPE_TESTS = [
    (int, int_type_test),
    (float, float_type_test),
    (datetime, datetime_type_test)
]

SQL_TYPE_DICT = {
    int: 'INT',
    float: 'DOUBLE',
    datetime: 'DATE',
    str: 'TEXT'
}

WINDOWS = 'Windows'
LINUX = 'Linux'
MAC_OS = 'Darwin'

PRE_SELECT_STMT = 'SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;'
POST_SELECT_STMT = 'SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;'
