import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QMainWindow)
from PyQt5.QtCore import QCoreApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.center()
        self.setWindowTitle('Test')
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

if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = Example()

    sys.exit(app.exec_())
