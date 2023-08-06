"""The purpose of this module is to provide functionality for interacting with services outside of this package.

These services should not be related to the core data management aspect of the package, and should instead be used
as extra functionality

"""
from datetime import datetime
from json import dumps
from socket import gethostname

from requests import post

from cfl_data_utils.database.rds_manager import RDSManager


def stub(*args, **kwargs):
    """Empty function

    Args:
        *args: Takes all non-default args
        **kwargs: Takes all default args
    """
    del args, kwargs  # Stubbed straight out


def slack(webhook_url, m):
    """Send a Slack message to a Slackbot

    Args:
        webhook_url (str): Webhook of Slackbot
        m (str): The message
    """
    post(webhook_url, headers={'Content-Type': 'application/json'}, json={'text': m})


def log(db_creds=None, db_obj=None, script=None, description=None, text_content=None, json_content: dict = None,
        numeric_content=None, boolean_content=None, tables_affected=None, num_rows_affected=None):
    """Logging utility to keep track of automated scripts

    Args:
        db_creds (dict): Credentials for connecting to the logging table
        db_obj (object): A pre-instantiated database object
        script (str): The script calling the log function
        description (str): A short description of the log
        text_content (str): Any useful/contextual text content
        json_content (dict): Any useful/contextual JSON content
        numeric_content (Union[int, float]): Any useful/contextual numeric content
        boolean_content (bool): Any useful/contextual boolean content
        tables_affected (list): A list of tables affected by the action
        num_rows_affected (int): Number of rows affected by the action

    Raises:
        ValueError: if there's no way of connecting to the database

        ValueError: if there's no content to log
    """
    if not (db_creds or hasattr(db_obj, 'conn')):
        raise ValueError('Unable to log. No valid database arguments passed.')

    if not (description or
            text_content or
            json_content or
            numeric_content or
            boolean_content is not None or
            tables_affected or
            num_rows_affected):
        raise ValueError('No content passed to logger. No entry made.')

    if not db_obj:
        db_obj = RDSManager(**db_creds)
        disconnect_db = True
    else:
        disconnect_db = False

    if not bool(db_obj.conn.open):
        db_obj.connect_to_db()

    script = f"'{script}'" if script is not None else 'NULL'
    description = f"'{description}'" if description is not None else 'NULL'
    text_content = "'{}'".format(text_content.replace("'", r"\'")) if text_content is not None else 'NULL'
    json_content = "'{}'".format(dumps(json_content).replace("'", r"\'")) if json_content is not None else 'NULL'
    tables_affected = f"'{dumps(tables_affected)}'" if tables_affected is not None else 'NULL'

    query = f"""
        INSERT INTO will_test.logs (source,
                                    script,
                                    timestamp,
                                    description,
                                    text_content,
                                    json_content,
                                    numeric_content,
                                    boolean_content,
                                    tables_affected,
                                    num_rows_affected)
        VALUES ('{gethostname()}',
                {script},
                TIMESTAMP '{datetime.now()}',
                {description},
                {text_content},
                {json_content},
                {numeric_content if numeric_content is not None else 'NULL'},
                {boolean_content if boolean_content is not None else 'NULL'},
                {tables_affected},
                {num_rows_affected if num_rows_affected is not None else 'NULL'});
          """

    db_obj.query(query)

    if disconnect_db:
        db_obj.disconnect(silent=True)
