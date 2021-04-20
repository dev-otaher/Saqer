import sqlite3
from sqlite3 import Error

from gui.Warning import Warning


class DBHelper:
    def create_db_connection(self, db_path: str):
        try:
            conn = sqlite3.connect(db_path)
            return conn
        except Error as e:
            Warning(str(e))
            print(e)
