import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 400, 200)

        button = QPushButton('Open Dialog', self)
        button.setGeometry(150, 100, 100, 30)
        button.clicked.connect(self.showDialog)

    def showDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Dialog Window')
        dialog.setGeometry(200, 200, 300, 150)

        label = QLabel('This is a dialog window', dialog)
        label.setGeometry(50, 50, 200, 30)

        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
