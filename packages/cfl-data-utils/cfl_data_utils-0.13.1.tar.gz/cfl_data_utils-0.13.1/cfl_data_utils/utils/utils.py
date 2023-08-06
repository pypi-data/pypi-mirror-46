"""
This module is for smaller utility function which are useful across many projects.

Todo:
    * better type testing using ``isinstance`` or ``assert``

"""
from datetime import datetime, timedelta
from os import get_terminal_size
from platform import system
from sys import stdout, modules
from time import time

from cfl_data_utils.references.constants import TYPE_TESTS, SQL_TYPE_DICT, WINDOWS

if not system() == WINDOWS:
    try:
        from blessings import Terminal
    except ModuleNotFoundError:
        from warnings import warn
        warn('Unable to import curses.')


def assert_date_is_yesterday(date):
    """Checks that a date is yesterday for data validation

    Args:
        date (datetime): The date to be validated

    Raises:
        AssertionError: if the date isn't today
    """
    yesterday = datetime.today() - timedelta(days=1)
    assert date.date() == yesterday.date()


def sqlize(string):
    """SQL-izes a string to ensure the characters are all legal

    Args:
        string (str): The string to be processed

    Returns:
        the processed SQL-friendly string
    """
    return string.upper().replace(' ', '_').replace('-', '_').replace(':', '_')


def get_var_type(value, sql=False):
    """Gets a Python type from a string variable

    Args:
        value (Union[int, float, str, datetime]): The variable to be type-checked
        sql (bool): Flag to decide if return type should be SQL-ized (e.g. int vs INT)

    Returns:
        Type of value passed in, either as SQL format ready for query of as Python type

    Examples:
        >>> get_var_type(123, sql=True)
        'INT'
    """
    for typ, test in TYPE_TESTS:
        try:
            test(value)
            return SQL_TYPE_DICT[typ] if sql else typ
        except (ValueError, AssertionError, TypeError):
            continue
    return 'TEXT' if sql else str


def increment_progress_display(processed=None, goal=100, start_time=None, downloaded=None, print_line=None,
                               terminal_width=None):
    """Displays a progress bar to track data processing progress

    Args:
        processed (int, optional): the amount of processing done so far (e.g. number of iterations)
        goal (int): the total amount of processing to be done
        start_time (float, optional): the time at which the processing was started
        downloaded (float, optional): amount of data downloaded
        print_line (int, optional): the line of the terminal to print the progress bar on
        terminal_width (int, optional): width of terminal used for sizing progress bar

    Returns:
        If the processed arg is passed in, it is incremented by 1 for use in while loops etc. where the counter can
        be incremented as part of this function.
        Alternatively, None is returned.
    """
    try:
        terminal_width = get_terminal_size()[0] if not terminal_width else terminal_width
    except OSError:
        terminal_width = 100

    def output():
        """Prints the progress bar to the terminal and increments processed parameter

        Returns:
            If the processed arg is passed in, it is incremented by 1 for use in while loops etc. where the counter can
            be incremented as part of this function.
            Alternatively, None is returned.
        """
        if processed:
            progressbar_width = 64 if terminal_width > 74 else terminal_width - 10
            progress = int(processed / (goal / progressbar_width))
            stdout.write(
                '|' +
                '#' * progress +
                '-' * (progressbar_width - progress) +
                f'| {(processed / goal) * 100:.2f}%  |  ' +
                f'{processed}/{goal} items  |  '
            )

        if start_time:
            time_elapsed = time() - start_time
            stdout.write(f'Time Elapsed: {timedelta(seconds=int(time_elapsed))}  |  ')
            if processed:
                stdout.write(f'Time remaining: '
                             f'{timedelta(seconds=int((time_elapsed / processed) * (goal - processed)))}'
                             f'  |  ')

            if downloaded:
                speed = f'{float((downloaded // (time() - start_time)) / 1000000):.3f}'
                stdout.write(f'Avg Speed: {speed} MB/s  |  ')

        if downloaded:
            stdout.write(f'Data processed: {downloaded / 1000000:.2f} MB')

        stdout.flush()

        return processed + 1 if processed is not None else None

    if not system() == WINDOWS and 'blessings' in modules:
        term = Terminal()
        with term.location(0, print_line):
            return output()
    else:
        return output()


def time_to_epoch(human_time=None, year=None, month=None, day=None, hour=None, minute=None, second=None):
    """Converts a time to an epoch timestamp

    It can take arguments of several different formats:
        - nothing can be passed, and the current epoch will be returned
        - each component part of the timestamp can be passed (e.g. year, month, day)
        - human_time is for more easily type-able time formats, e.g. 19700101120000 or 1970-01-01 12:00:00

    Args:
        human_time (str): a more human-readable time to allow easier entry
        year (int): year to be converted
        month (int): month to be converted
        day (int): day to be converted
        hour (int): hour to be converted
        minute (int): minute to be converted
        second (int): second to be converted

    Returns:
        The time passed in (or the current time otherwise) as time since epoch in seconds
    """

    year = datetime.now().year if year is None else year
    month = datetime.now().month if month is None else month
    day = datetime.now().day if day is None else day
    hour = datetime.now().hour if hour is None else hour
    minute = datetime.now().minute if minute is None else minute
    second = datetime.now().second if second is None else second

    if human_time:
        if isinstance(human_time, int) or get_var_type(human_time) == int:
            human_time_str = str(human_time)
            if len(human_time_str) == 8:  # YYYYMMDD
                time_elem_list = [human_time_str[:4], human_time_str[4:6], human_time_str[6:8], '00', '00', '00']
            elif len(human_time_str) == 12:  # YYYYMMDDHHMM
                time_elem_list = [human_time_str[:4], human_time_str[4:6], human_time_str[6:8], human_time_str[8:10],
                                  human_time_str[10:], '00']
            elif len(human_time_str) == 13:  # Probably passed epoch time by accident
                return human_time
            elif len(human_time_str) == 14:  # YYYYMMDDHHMMSS
                time_elem_list = [human_time_str[:4], human_time_str[4:6], human_time_str[6:8], human_time_str[8:10],
                                  human_time_str[10:12], human_time_str[12:]]
            else:
                raise ValueError(f'Invalid human_time passed: {human_time}\n'
                                 f'Use this format: YYYYMMDDHHMMSS | YYYY-MM-DD HH:MM:SS')
        else:
            time_elem_list = human_time.split('-')[:-1] + human_time.split('-')[-1].split()[:-1] + \
                             human_time.split('-')[-1].split()[-1].split(':')

            if not len(time_elem_list) == 6:
                raise ValueError(f'Invalid human_time passed: {human_time}\n'
                                 f'Use this format: YYYYMMDDHHMMSS | YYYY-MM-DD HH:MM:SS')

        str_year = time_elem_list[0]
        str_month = time_elem_list[1]
        str_day = time_elem_list[2]
        str_hour = time_elem_list[3]
        str_minute = time_elem_list[4]
        str_second = time_elem_list[5]
    else:
        str_year = str(year)
        str_month = str(month).rjust(2, '0')
        str_day = str(day).rjust(2, '0')
        str_hour = str(hour).rjust(2, '0')
        str_minute = str(minute).rjust(2, '0')
        str_second = str(second).rjust(2, '0')

    try:
        return int(
            datetime.strptime(
                f'{str_year} {str_month} {str_day} {str_hour} {str_minute} {str_second}',
                '%Y %m %d %H %M %S'
            ).timestamp()
        ) * 1000
    except ValueError:
        raise ValueError(
            f'Invalid arguments passed to time_to_epoch function. Strings: '
            f'{str_year} {str_month} {str_day} {str_hour} {str_minute} {str_second}'
        )


def get_col_types(data, sql=False):
    """Returns column headers and their types from a CSV or JSON file

    Args:
        data (Union[BufferedReader, BufferedWriter, TextIOWrapper, str, dict]): the file to be parsed
        sql (bool): flag to say whether the types should be in SQL dialect or not

    Returns:
        List:
            A list of two-element dictionaries (column name and value type). For example::
                [{name: 'col1', type: 'typ1'},
                {name: 'col2', type: 'typ2'},
                {name: 'col3', type: 'typ3'}]

            The types can either be Python types or their SQL dialect counterparts (str vs 'TEXT')
    """

    cols = None
    first_rows = []
    try:
        with open(data) as f:
            for i, row in enumerate(f):
                if i == 0:
                    cols = row.rstrip('\n').split(',')
                elif 0 < i < 20:
                    first_rows.append(row.rstrip('\n').split(','))
                else:
                    break
    except TypeError:
        cols = list(data[0].keys())
        first_rows = [None] * 20
        i = 0
        while i < len(first_rows):
            first_rows[i] = list(data[i].values())
            i += 1

    col_type_list = []
    for i, col in enumerate(cols):
        type_found = False
        for row in first_rows:
            if not (row[i] == '' or row[i] is None):  # pylint: disable=unsubscriptable-object
                type_found = True
                col_type_list.append(
                    {'name': col, 'type': get_var_type(row[i], sql)}  # pylint: disable=unsubscriptable-object
                )
                break
        if not type_found:
            col_type_list.append({'name': col, 'type': get_var_type('', sql)})

    return col_type_list
