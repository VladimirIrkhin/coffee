import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QMessageBox
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.loadTable()
        self.change_button.clicked.connect(self.interact_with_table)
        self.add_button.clicked.connect(self.interact_with_table)
        self.current_ides = []

    def loadTable(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        data = cur.execute('SELECT * FROM main_table ORDER BY id').fetchall()
        con.close()

        self.coffee_table.setRowCount(0)
        for i, row in enumerate(data):
            self.coffee_table.setRowCount(self.coffee_table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.coffee_table.setItem(i, j, QTableWidgetItem(str(elem)))

        self.current_ides = [i[0] for i in data]

    def interact_with_table(self):
        if self.sender().text() == 'Добавить':
            self.second_form = addEditCoffeeForm(parent=self)
        elif self.sender().text() == 'Изменить':
            values = [self.coffee_table.item(self.coffee_table.currentRow(), i).text() for i in range(7)]
            self.second_form = addEditCoffeeForm(values=values, parent=self)
        self.setEnabled(False)
        self.second_form.show()
        self.second_form.setEnabled(True)


class addEditCoffeeForm(QMainWindow):
    def __init__(self, values=None, parent=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.values = values
        self.lineEdits = [self.lineEdit_id, self.lineEdit_type, self.lineEdit_degree, self.lineEdit_grand_or_whole,
                          self.lineEdit_taste, self.lineEdit_price, self.lineEdit_volume]
        self.initUI()

    def initUI(self):
        if self.values:
            for value, lineEdit in zip(self.values, self.lineEdits):
                lineEdit.setText(str(value))
            self.lineEdit_id.setEnabled(False)
            self.interact_button.setText('Изменить')
        else:
            self.interact_button.setText('Добавить')
        self.interact_button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        if self.check_correctness():
            if self.values:
                self.delete()
            self.add()
            self.parent().loadTable()
            self.close()
        else:
            QMessageBox.warning(self, '', 'Значения некорректны!')
            pass

    def check_correctness(self):
        try:
            if all([i.text() for i in self.lineEdits[1:5]]) and [int(self.lineEdit_id.text())] and\
                    [[float(i.text())] for i in self.lineEdits[5:]]:
                return True
            return False
        except ValueError:
            return False

    def delete(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute(f'DELETE FROM main_table WHERE id = {self.values[0]}')
        con.commit()
        con.close()

    def add(self):
        new_values = [i.text() for i in self.lineEdits]
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute(f'''INSERT INTO main_table(id, type, degree, ground_or_whole, taste, price, volume) 
        VALUES({new_values[0]}, "{new_values[1]}", "{new_values[2]}", "{new_values[3]}", "{new_values[4]}",
        {new_values[5]}, {new_values[6]})''')
        con.commit()
        con.close()

    def closeEvent(self, e):
        self.parent().setEnabled(True)
        e.accept()
        QWidget.closeEvent(self, e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
