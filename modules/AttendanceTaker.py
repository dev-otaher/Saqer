from sqlite3.dbapi2 import Error
from typing import List

from modules.DBHelper import DBHelper
from modules.Student import Student
from modules.Students import Students


class AttendanceTaker:
    def __init__(self, class_id):
        self.class_id = class_id
        self.students = Students()
        self.checkpoints = 0
        self.db = DBHelper()
        self.db_conn = DBHelper().create_db_connection("db/saqer.db")

    def connection_is_open(self):
        try:
            self.db_conn.execute("SELECT 1 FROM student LIMIT 1;")
            return True
        except Error:
            return False

    def create_connection(self):
        self.db_conn = self.db.create_db_connection("db/saqer.db")

    def populate_std_list(self):
        sql = '''
                SELECT s.uni_id, s.name FROM enroller as e
                INNER JOIN student as s 
                ON e.student_id = s.uni_id
                WHERE e.class_id = ?
                '''
        if self.connection_is_open() is False:
            self.create_connection()
        cur = self.db_conn.cursor()
        cur.execute(sql, (self.class_id,))
        records = cur.fetchall()
        for r in records:
            self.students.append(Student(str(r[0]), str(r[1])))
        return self

    def get_std_by_id(self, std_id) -> Student:
        for std in self.students:
            if std.uni_id == std_id:
                return std

    def get_id_by_name(self, std_name: str):
        for std in self.students:
            if std.name == std_name:
                return std.uni_id

    def increment(self, std: Student):
        std.appear_counter += 1

    def increment_checkpoint(self):
        self.checkpoints += 1
