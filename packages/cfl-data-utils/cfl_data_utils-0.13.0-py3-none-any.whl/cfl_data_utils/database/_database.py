#!/usr/bin/env python
"""Extendable Database class for connecting to different database types within Chetwood Financial.

TODO
    * Implement time out functionality for reducing idle connections
"""

from os import path
from warnings import warn

from pandas import read_sql_query, DataFrame
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

__author__ = 'Will Garside'
__email__ = 'worgarside@gmail.com'
__status__ = 'Production'


class Database:
    """Base database class

    This is to be used as a super class by different database connectors

    Attributes:
        db_name (str): Name of the database to connect to
        ssh_host (str): Host IP of the SSH tunnel
        ssh_username (str): User for access to SSH tunnel
        pkey_path (str): Path to the .pem file containing the PKey
        db_bind_address (str): Binding address for the database
        db_user (str): Database username
        db_password (str): Database password
        db_host (str): Host IP for the database, usually 127.0.0.1 after SSH tunneling
        db_port (int): DB port
        ssh_port (int): SSH Tunnel port, defaults to 22
        stubbed (bool): Flag to stub database calls
        max_idle_time (int): Maximum time connection can idle before being disconnected
     """

    def __init__(self, ssh_host=None, ssh_port=22, ssh_username=None, pkey_path=None, db_name=None,
                 db_bind_address=None, db_host='127.0.0.1', db_port=None, db_user=None, db_password=None, stubbed=False,
                 max_idle_time=30, disable_ssh_tunnel=False):
        """Inits Database and validates setup config"""

        self.conn = None
        self.cur = None
        self.server = None
        self.dialect = None
        self.driver = None

        self.error_state = False
        self.stubbed = stubbed
        self.max_idle_time = max_idle_time

        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_bind_address = db_bind_address

        self.ssh_host = ssh_host
        self.ssh_port = int(ssh_port)
        self.ssh_username = ssh_username
        self.pkey_path = pkey_path

        self.required_creds = {}

        if self.stubbed:
            print(f'\033[31mWarning: Connection to \033[1m{self.db_name}\033[31m is stubbed.'
                  f' No data will be affected.\033[0m')

        self.setup()
        self.validate_setup(disable_ssh_tunnel)
        self.connect_to_db(disable_ssh_tunnel)

    def setup(self):
        """Allows each database subclass to be setup differently according to the relevant dialect and driver"""

    def connect_to_db(self, disable_ssh_tunnel):
        """Placeholder method for the actual connection to the DB

        Args:
            disable_ssh_tunnel (bool): Determines whether an SSH tunnel should be used
        """

    def validate_setup(self, disable_ssh_tunnel):
        """Validate the setup of the database: args, connections etc.

        Args:
            disable_ssh_tunnel (bool): Determines whether an SSH tunnel should be used
        """

        missing_params = [k for k, v in self.__dict__.items() if not v and k in self.required_creds]

        if missing_params:
            self.error_state = True
            raise TypeError(f"Database instance missing params: {missing_params}")

        if not disable_ssh_tunnel and self.pkey_path and not path.isfile(self.pkey_path):
            self.error_state = True
            raise IOError(f"{self.pkey_path} is not a valid file."
                          f" Make sure you have provided the absolute path")

    def query(self, sql, commit=True):
        """Executes a query passed in by using the DatabaseManager object

        Args:
            sql (str): The sql query to be executed by the Cursor object
            commit (bool): Committing on queries can be disabled for rapid writing (e.g. q_one commit at end)

        Returns:
            the Cursor object for continued usage
        """

        if self.stubbed:
            return self.cur

        self.cur.execute(sql)
        if commit:
            self.commit()
        return self.cur

    def df_from_query(self, stmt, index_col=None, coerce_float=True, params=None, parse_dates=None, chunksize=None):
        """Generates a pandas dataframe from an SQL query. All parameter defaults match those of read_sql_query.

        Args:
            stmt (str): The query to be executed by the Cursor object
            index_col (Union[Iterable[str], str]): Column(s) to set as index(MultiIndex).
            coerce_float (bool): Attempts to convert values of non-string, non-numeric objects (like decimal.Decimal)
                to floating point. Useful for SQL result sets.
            params (Union[List, Tuple, Dict]): List of parameters to pass to execute method.  The syntax used to pass
                parameters is database driver dependent.
            parse_dates (Union[List, Dict]):
                - List of column names to parse as dates.
                - Dict of ``{column_name: format string}`` where format string is
                  strftime compatible in case of parsing string times, or is one of
                  (D, s, ns, ms, us) in case of parsing integer timestamps.
                - Dict of ``{column_name: arg dict}``, where the arg dict corresponds
                  to the keyword arguments of :func:`pandas.to_datetime`
                  Especially useful with databases without native Datetime support,
                  such as SQLite.
            chunksize (int): If specified, return an iterator where `chunksize` is the number of rows to include in
                each chunk.

        Returns:
            DataFrame object
        """
        if self.stubbed:
            return DataFrame()

        df: DataFrame = read_sql_query(stmt, self.conn, index_col=index_col, coerce_float=coerce_float, params=params,
                                       parse_dates=parse_dates, chunksize=chunksize)
        return df

    def df_to_table(self, df, name, schema=None, if_exists='fail', index=True, index_label=None, chunksize=None,
                    dtype=None, method=None):
        """Write records stored in a DataFrame to a SQL database.

        Args:
            df (DataFrame): DataFrame to convert
            name (str): Name of table to be created
            schema (str): Specify the schema (if database flavor supports this)
            if_exists (str): How to behave if the table already exists
            index (bool): Write DataFrame index as a column. Uses index_label as the column name in the table.
            index_label (Union[str, List]): Column label for index column(s). If None is given (default) and index
                is True, then the index names are used. A sequence should be given if the DataFrame uses MultiIndex.
            chunksize (int): Rows will be written in batches of this size at a time. By default, all rows will be
                written at once.
            dtype (dict): Specifying the datatype for columns. The keys should be the column names and the values
                should be the SQLAlchemy types or strings for the sqlite3 legacy mode.
            method (Union[None, str, callable]): Controls the SQL insertion clause used:
                None : Uses standard SQL INSERT clause (one per row).
                ‘multi’: Pass multiple values in a single INSERT clause.
                callable with signature (pd_table, conn, keys, data_iter)
        """
        if self.stubbed:
            return

        if if_exists not in {None, 'fail', 'replace', 'append'}:
            warn(f"Parameter if_exists has invalid value: {if_exists}. "
                 f"Should be one of {{None, 'fail', 'replace', 'append'}}")
            if_exists = None

        if isinstance(method, str) and not method == 'multi':
            warn(f"Parameter method has invalid value: {method}. Should be one of {{None, 'multi', callable}}")
            method = None

        engine = create_engine(
            URL(
                drivername=f'{self.dialect}+{self.driver}',
                username=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name
            )
        )

        df.to_sql(name=name, con=engine, schema=schema, if_exists=if_exists, index=index, index_label=index_label,
                  chunksize=chunksize, dtype=dtype, method=method)

    def executemany(self, stmt: str, data):
        """

        Args:
            stmt (str): The query to be executed by the Cursor object
            data (Union[List, Tuple]): The data to be processed

        Returns:
            the Cursor object for continued usage
        """
        if self.stubbed:
            return self.cur

        self.cur.executemany(stmt, data)
        return self.cur

    def commit(self):
        """Commits all changes to database

        Returns:
            the Cursor object for continued usage
        """

        self.conn.commit()
        return self.cur

    def disconnect(self, silent: bool = False):
        """Disconnects from the database and the SSH tunnel

        Args:
            silent (bool): suppresses final print statement
        """
        self.conn.close()
        if self.server is not None:
            self.server.close()
        if not silent:
            print(f"{self.db_name if self.db_name else 'Database'} disconnected.")
