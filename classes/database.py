import mysql.connector
from settings import *

class Database:

    host = MYSQL_HOST
    user = MYSQL_USER
    password = MYSQL_PASSWORD
    db = 'mlbstats'

    def __init__(self):
        self.connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.db)
        self.cursor = self.connection.cursor()

    def insert(self, query, *args, **kwargs):
        try:
            if 'many' in kwargs and kwargs['many'] == True:
                self.cursor.executemany(query, *args)
            else:
                self.cursor.execute(query, *args)
            self.connection.commit()
        except mysql.connector.Error as err:
          print("Something went wrong: {}".format(err))
          self.connection.rollback()

    def query(self, query, *args):
        cursor = self.connection.cursor()
        cursor.execute(query, *args)

        return cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
