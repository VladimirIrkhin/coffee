import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.loadTable()

    def loadTable(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        data = cur.execute('SELECT * FROM main_table').fetchall()
        con.close()

        self.coffee_table.setRowCount(0)
        for i, row in enumerate(data):
            self.coffee_table.setRowCount(self.coffee_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.coffee_table.setItem(i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
