from sqlite3 import Error
from qtpy import QtWidgets
from gui.Warning import Warning


class ViewReports:
    def __init__(self, parent_gui):
        self.parent = parent_gui
        self.connect_widgets()
        self.hide_widgets()
        self.db_conn = self.parent.db.create_db_connection("db/saqer.db")
        self.fill_table()

    def connect_widgets(self):
        pass
        # self.parent.i_courses_table.clicked.connect(self.start_offline_attendance)
        # self.parent.i_save_recheck.clicked.connect(self.save_data)

    def hide_widgets(self):
        self.parent.i_save_recheck.setHidden(True)

    def fill_table(self):
        try:
            print(self.parent.UUID)
            sql = '''
                    SELECT DISTINCT	course.code, course.title FROM class 
                    INNER JOIN course ON class.course_id == course.id 
                    WHERE instructor_id=?;
                    '''
            cur = self.db_conn.cursor()
            cur.execute(sql, (self.parent.UUID,))
            courses = cur.fetchall()

            for course in courses:
                self.parent.i_courses_table.insertRow(0)
                self.parent.i_courses_table.setItem(0, 0, QtWidgets.QTableWidgetItem(course[0]))
                self.parent.i_courses_table.setItem(0, 1, QtWidgets.QTableWidgetItem(course[1]))

            #     id = self.parent.i_recheck_table.item(r, 0).text()
            #     status = self.parent.i_recheck_table.cellWidget(r, 3).isChecked()
            #     cur.execute(sql, (id, status))
            #     self.db_conn.commit()
        except Error as e:
            Warning(str(e))
            print(e)

        # pass
        # classes = [{"Name": "CS411", "Title": "Data Structure", "Time": "1:00 - 3:00 PM"},
        #            {"Name": "CIS432", "Title": "Operating Systems", "Time": "1:00 - 3:00 PM"}]
        # row = 0
        # self.parent.i_courses_table.setRowCount(len(classes))
        # for person in classes:
        #     self.parent.i_courses_table.setItem(row, 0, QtWidgets.QTableWidgetItem(person["Name"]))
        #     self.parent.i_courses_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(person["Title"])))
        #     self.parent.i_courses_table.setItem(row, 2, QtWidgets.QTableWidgetItem(person["Time"]))
        #     row = row + 1

    def format_table(self):
        self.parent.i_recheck_table.setColumnWidth(0, 212)
        self.parent.i_recheck_table.setColumnWidth(1, 212)
        self.parent.i_recheck_table.setColumnWidth(2, 212)
        self.parent.i_recheck_table.setColumnWidth(3, 212)

    def reset_table(self):
        self.parent.i_recheck_table.clearContents()
        self.parent.i_recheck_table.setRowCount(0)

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
