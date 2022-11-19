import sqlite3
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, \
    QDialog, QWidget
import UI


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class Window(QWidget, UI.MainUI):
    def __init__(self):
        super(Window, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_row_in_table)
        self.tableWidget.itemDoubleClicked.connect(self.elem_double_clicked)
        self.load_table()

    def load_table(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        res = cur.execute('select * from coffee').fetchall()
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                if isinstance(elem, int):
                    elem = str(elem)
                item = QTableWidgetItem(elem)
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.tableWidget.setItem(i, j, item)
        self.tableWidget.resizeColumnsToContents()

    def add_row_in_table(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        for i in range(self.tableWidget.columnCount()):
            item = QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, i, item)

    def elem_double_clicked(self, item):
        row = item.row()
        was_empty = not bool(self.tableWidget.item(row, 0).text())
        dialog = MyDialog(self.tableWidget.item(row, 0).text(), was_empty)
        if dialog.exec_():
            self.load_table()


class MyDialog(QDialog, UI.DialogUI):
    def __init__(self, coffee_id, was_empty=True):
        super(MyDialog, self).__init__()
        self.setupUi(self)
        self.ok_btn.setDefault(True)
        self.was_empty = was_empty
        self.id = coffee_id
        self.name = ''
        self.roast = ''
        self.wh = ''
        self.taste = ''
        self.count = ''
        self.vol = ''
        self.ok_btn.clicked.connect(self.save_and_close)
        self.ne_ok_btn.clicked.connect(self.reject)

    def save_and_close(self):
        self.id = None if self.was_empty else self.id
        self.name = self.le2.text()
        self.roast = self.le3.text()
        self.wh = self.le4.text()
        self.taste = self.le5.text()
        self.count = self.le6.text()
        self.vol = self.le7.text()
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        if not self.was_empty:
            cur.execute('update coffee set name = ? where id = ?',
                        (self.name, self.id))
            cur.execute('update coffee set roasting = ? where id = ?',
                        (self.roast, self.id))
            cur.execute('update coffee set wholeness = ? where id = ?',
                        (self.wh, self.id))
            cur.execute('update coffee set taste = ? where id = ?',
                        (self.taste, self.id))
            cur.execute('update coffee set count = ? where id = ?',
                        (self.count, self.id))
            cur.execute('update coffee set volume = ? where id = ?',
                        (self.vol, self.id))
        else:
            cur.execute(
                '''insert into coffee(id, name, roasting, wholeness, 
taste, count, volume) values (?, ?, ?, ?, ?, ?, ?)''',
                (self.id, self.name, self.roast, self.wh, self.taste,
                 self.count, self.vol))
        con.commit()
        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
