import sys

from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication,
    QLabel, QLineEdit, QWidget, QGridLayout, QMessageBox, QDesktopWidget)
from PyQt5.QtGui import QIcon

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
        part_label = QLabel("Part")
        quantity_edit = QLineEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(part_label, 1, 0)
        grid.addWidget(quantity_edit, 1, 1)

        self.setLayout(grid)
        

if __name__ == '__main__':

    APP = QApplication(sys.argv)
    ex = AutoOrder()
    sys.exit(APP.exec_())
