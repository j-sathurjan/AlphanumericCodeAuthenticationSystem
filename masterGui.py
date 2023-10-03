from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200,100,500,500)
    win.setWindowTitle("Master GUI")
    win.show()
    sys.exit(app.exec_())
    
window()