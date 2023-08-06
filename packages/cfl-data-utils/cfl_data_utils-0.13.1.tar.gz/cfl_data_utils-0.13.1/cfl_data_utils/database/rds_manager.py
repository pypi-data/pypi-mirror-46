#!/usr/bin/env python
"""Provides the RDSManager class to connect to the existing AWS RDS in use by CFL"""
from os import getenv
from socket import gethostname
from time import sleep

from pymysql import connect
from pymysql.err import OperationalError
from sshtunnel import SSHTunnelForwarder

from ._database import Database

__author__ = 'Will Garside'
__email__ = 'worgarside@gmail.com'
__status__ = 'Production'


class RDSManager(Database):
    """Extension of the Database class specifically for connecting to a MySQL AWS RDS"""

    def setup(self):
        """Setup the SSH Tunnel and Database connection"""

        self.dialect = 'mysql'
        self.driver = 'pymysql'
        self.required_creds = {'db_user'}
        self.db_port = 3306 if not self.db_port else self.db_port

    def _open_ssh_tunnel(self):
        """The RDS requires SSH tunnelling in, so this does that"""

        tunnel_success = False

        while not tunnel_success:
            try:
                self.server = SSHTunnelForwarder(
                    (self.ssh_host, self.ssh_port),
                    ssh_username=self.ssh_username,
                    ssh_pkey=self.pkey_path,
                    remote_bind_address=(self.db_bind_address, self.db_port)
                )
                tunnel_success = True
            except KeyboardInterrupt:
                self.disconnect()
            sleep(5)

        self.server.start()

    def connect_to_db(self, disable_ssh_tunnel=False):
        """Open the connection to the database

        Args:
            disable_ssh_tunnel (bool): Determines whether an SSH tunnel should be used
        """
        try:
            if not disable_ssh_tunnel:
                self._open_ssh_tunnel()
                self.db_port = self.server.local_bind_port
        except ValueError:  # No password or public key available!
            # ValueError is raised because there's no creds for the SSH Tunnel (because we're already on the EC2),
            # so just continue without SSHing in if we are on the EC2
            if not gethostname() == getenv('RDS_EC2_HOSTNAME'):
                raise

        connection_success = False

        while not connection_success:
            try:
                self.conn = connect(
                    user=self.db_user,
                    passwd=self.db_password,
                    host=self.db_host,
                    database=self.db_name,
                    port=self.db_port
                )
                connection_success = True
                self.cur = self.conn.cursor()
            except KeyboardInterrupt:
                self.disconnect()
            except OperationalError:
                if gethostname() == getenv('RDS_EC2_HOSTNAME') and not self.db_host == self.db_bind_address:
                    self.db_host = self.db_bind_address
                    print('Resetting db_host')
                else:
                    raise
            sleep(5)
