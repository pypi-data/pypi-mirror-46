"""The purpose of this module is to provide functionality for interacting with services outside of this package.

These services should not be related to the core data management aspect of the package, and should instead be used
as extra functionality

"""
from io import StringIO
from boto3 import client
from datetime import datetime
from json import dumps
from socket import gethostname

from requests import post

from cfl_data_utils.database.rds_manager import RDSManager
from cfl_data_utils.utils.bytes_io_wrapper import BytesIOWrapper


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


def df_to_s3_csv(df, bucket_name, access_key, secret_key, file_ref, force_leading_slash=False, **kwargs):
    """Upload a DataFrame to an S3 bucket as a CSV

    Args:
        df: The DataFrame to be uploaded
        bucket_name: Name of the S3 bucket to receive the file
        access_key: AWS access key
        secret_key: AWS secret key
        file_ref: the 'directories' and the name of the file being uploaded
        force_leading_slash: Forces the upload to occur with a leading slash on the file_ref. May create unnamed
        directory.
    """

    assert force_leading_slash or not file_ref.startswith('/'), \
        f"Can't upload file with leading slash: '{file_ref}'. If this is intended, add the " \
        "`force_leading_slash=True` argument."""

    csv_buf = StringIO()

    df.to_csv(csv_buf, index=False, **kwargs)
    csv_buf.seek(0)

    s3_client = client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    s3_client.upload_fileobj(BytesIOWrapper(csv_buf), bucket_name, file_ref)
