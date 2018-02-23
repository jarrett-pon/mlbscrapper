"""Database class for all queries."""
import mysql.connector
from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST


class Database:
    """Database class."""

    host = MYSQL_HOST
    user = MYSQL_USER
    password = MYSQL_PASSWORD
    db = 'mlbstats'

    def __init__(self):
        """Init function for database class."""
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db
        )
        self.cursor = self.connection.cursor()

    def insert(self, query, *args, **kwargs):
        """Insert function for sql statements."""
        try:
            if 'many' in kwargs and kwargs['many'] is True:
                self.cursor.executemany(query, *args)
            else:
                self.cursor.execute(query, *args)
            self.connection.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            self.connection.rollback()

    def query(self, query, *args):
        """Query function for sql select statements."""
        cursor = self.connection.cursor()
        cursor.execute(query, *args)

        return cursor.fetchall()

    def __del__(self):
        """When class is __del__ then close connection."""
        self.cursor.close()
        self.connection.close()
