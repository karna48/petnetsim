from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
import editor
import petnetsim


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('editor/petnetsim.ui', self)

        #self.editor = editor.Editor()
        #self.setCentralWidget(self.editor)



def run():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    app.exec()


if __name__ == '__main__':
    run()
