import sys
import jsonparse

from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication, QPushButton,
    QLabel, QLineEdit, QWidget, QGridLayout, QMessageBox, QDesktopWidget)
from PyQt5.QtGui import QIcon, QIntValidator

class AutoOrder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.partspage = PartsPage()
        self.setCentralWidget(self.partspage)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('AutoOrder')
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Quit?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class PartsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        line_edit_array = []
        row_counter = 0
        items = jsonparse.getParts()

        validator = QIntValidator(self)

        for item in items:
            part_label = QLabel(item["Description"])

            quantity_edit = QLineEdit()
            quantity_edit.setValidator(validator)

            crm_number = QLabel(item["SKU"])

            line_edit_array.append(quantity_edit)

            grid.addWidget(part_label, row_counter, 0)
            grid.addWidget(quantity_edit, row_counter, 1)
            grid.addWidget(crm_number, row_counter, 2)

            row_counter = row_counter + 1

        submit_btn = QPushButton("&Submit", self)
        submit_btn.clicked.connect(lambda: filterArray(items, line_edit_array))
        grid.addWidget(submit_btn, row_counter, 0, 1, 3)
        self.setLayout(grid)

def filterArray(items, entry_array):
    selected_items = []
    count = 0
    for item in items:
        quantity = entry_array[count].text()
        print(quantity)
        if quantity != "":
            selected_items.append((item, quantity))
        count = count + 1
    
    for entry in entry_array:
        entry.setText("")
    
    print(selected_items)


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    ex = AutoOrder()
    sys.exit(APP.exec_())
