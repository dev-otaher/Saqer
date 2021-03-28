from typing import List

from modules.Student import Student
from modules.Students import Students


class AttendanceTaker:
    def __init__(self, class_id="", date=""):
        self.class_id = class_id
        self.date = date
        self.students: Students

    def populate_std_list(self):
        omar = Student("2170007761", "Omar")
        khalid = Student("2170007739", "Khalid")
        waleed = Student("2170003286", "Waleed")
        self.students = [omar, khalid, waleed]
        return self

    def get_std_by_id(self, std_id) -> Student:
        for std in self.students:
            if std.uni_id == std_id:
                return std

    def get_id_by_name(self, std_name:str):
        for std in self.students:
            if std.name == std_name:
                return std.uni_id

    def increment(self, std: Student):
        std.appear_counter += 1
