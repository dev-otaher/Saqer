from sqlite3 import Error
from qtpy import QtWidgets
from gui.Warning import Warning


class ViewReports:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.connect_widgets()
        self.hide_widgets()
        self.db_conn = self.parent.db.create_db_connection("db/saqer.db")
        self.fill_courses()

    def connect_widgets(self):
        self.parent.i_courses_table.clicked.connect(self.fill_classes)
        # self.parent.i_save_recheck.clicked.connect(self.save_data)

    def hide_widgets(self):
        self.parent.i_save_recheck.setHidden(True)
        self.parent.i_courses_table.setColumnHidden(0, True)
        self.parent.i_classes_table.setColumnHidden(0, True)

    def fill_courses(self):
        try:
            sql = '''
                    SELECT DISTINCT	course.id, course.code, course.title FROM class 
                    INNER JOIN course ON class.course_id == course.id 
                    WHERE instructor_id=?;
                    '''
            cur = self.db_conn.cursor()
            cur.execute(sql, (self.parent.UUID,))
            courses = cur.fetchall()
            for course in courses:
                self.add_course(course)
        except Error as e:
            Warning(str(e))
            print(e)

    def add_course(self, course):
        self.parent.i_courses_table.insertRow(0)
        self.parent.i_courses_table.setItem(0, 0, QtWidgets.QTableWidgetItem(str(course[0])))
        self.parent.i_courses_table.setItem(0, 1, QtWidgets.QTableWidgetItem(course[1]))
        self.parent.i_courses_table.setItem(0, 2, QtWidgets.QTableWidgetItem(course[2]))

    def fill_classes(self, location):
        try:
            row = location.row()
            course_id = self.parent.i_courses_table.item(row, 0).text()
            sql = '''
                    SELECT id, title, date, time FROM class 
                    WHERE course_id=?;
                    '''
            cur = self.db_conn.cursor()
            cur.execute(sql, (course_id,))
            classes = cur.fetchall()
            self.reset_table(self.parent.i_classes_table)
            for c in classes:
                self.add_class(c)

            self.parent.goto(self.parent.i_stacked_widget, self.parent.i_classes)
            self.parent.i_title.setText("View Reports - Classes")


            # classes = [
            #     {"Attendance1": "Attendance Reports", "Behaviour": "Behaviour Reports", "Attendance": "09/01/2020",
            #      "From": "1:00 PM", "To": "03:00 PM"},
            #     {"Attendance1": "Attendance Reports", "Behaviour": "Behaviour Reports", "Attendance": "10/01/2020",
            #      "From": "8:00 PM", "To": "10:00 PM"},
            #     {"Attendance1": "Attendance Reports", "Behaviour": "Behaviour Reports", "Attendance": "11/01/2020",
            #      "From": "12:00 PM", "To": "03:00 PM"}]
            # row = 0
            # self.i_classes_table.setRowCount(len(classes))
            # for person in classes:
            #     atten = QtWidgets.QTableWidgetItem(person["Attendance1"])
            #     atten.setForeground(QColor(56, 219, 208))
            #     behv = QtWidgets.QTableWidgetItem(person["Behaviour"])
            #     behv.setForeground(QColor(56, 219, 208))
            #     rest = QtWidgets.QTableWidgetItem(person["Attendance"])
            #     rest2 = QtWidgets.QTableWidgetItem(person["From"])
            #     rest3 = QtWidgets.QTableWidgetItem(person["To"])
            #
            #     rest.setForeground(QColor(255, 255, 255))
            #     rest2.setForeground(QColor(255, 255, 255))
            #     rest3.setForeground(QColor(255, 255, 255))
            #
            #     self.i_classes_table.setItem(row, 0, atten)
            #     self.i_classes_table.setItem(row, 1, behv)
            #     self.i_classes_table.setItem(row, 2, rest)
            #     self.i_classes_table.setItem(row, 3, rest2)
            #     self.i_classes_table.setItem(row, 4, rest3)
            #     row = row + 1
            # self.i_classes_table.clicked.connect(self.show_behaviour)
        except Error as e:
            Warning(str(e))
        except Exception as e:
            print(e)

    def add_class(self, c):
        self.parent.i_classes_table.insertRow(0)
        self.parent.i_classes_table.setItem(0, 0, QtWidgets.QTableWidgetItem(str(c[0])))
        self.parent.i_classes_table.setItem(0, 2, QtWidgets.QTableWidgetItem(c[1]))
        self.parent.i_classes_table.setItem(0, 3, QtWidgets.QTableWidgetItem(c[2]))
        self.parent.i_classes_table.setItem(0, 4, QtWidgets.QTableWidgetItem(c[3]))

    def reset_table(self, table):
        table.clearContents()
        table.setRowCount(0)

    def save_data(self):
        try:
            sql = '''INSERT INTO attendence (student_id, status)
                            VALUES (?, ?)'''
            cur = self.db_conn.cursor()
            for r in range(self.parent.i_recheck_table.rowCount()):
                id = self.parent.i_recheck_table.item(r, 0).text()
                status = self.parent.i_recheck_table.cellWidget(r, 3).isChecked()
                cur.execute(sql, (id, status))
                self.db_conn.commit()
        except Error as e:
            Warning(str(e))
            print(e)
