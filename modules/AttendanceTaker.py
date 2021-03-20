from modules.Student import Student


class AttendanceTaker:
    def __init__(self, class_id="", date=""):
        self.class_id = class_id
        self.date = date
        self.students = set()

    def populate_student_list_from_db(self):
        omar = Student("2170007761", "Omar Ahmed")
        khalid = Student("2170007739", "Khalid Awlaqi")
        waleed = Student("2170003286", "Waleed Al-Harthi")
        self.students = {omar, khalid, waleed}
        return self

    def find_student_by_id(self, student_id):
        if student_id in self.students:
            print(student_id)


if __name__ == '__main__':
    taker = AttendanceTaker().populate_student_list_from_db()
    print(taker.find_student_by_id("2170007761"))
