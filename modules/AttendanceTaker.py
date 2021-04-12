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
        self.faces = 0
        self.db = DBHelper()
        self.db_conn = DBHelper().create_db_connection("db/saqer.db")

    def populate_std_list(self):
        sql = '''
                SELECT s.uni_id, s.name FROM enroller as e
                INNER JOIN student as s 
                ON e.student_id = s.uni_id
                WHERE e.class_id = ?
                '''
        with self.db_conn as con:
            records = con.cursor().execute(sql, (self.class_id,)).fetchall()
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

    def increment_faces(self):
        self.faces += 1
