from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
import editor


# class Simulation:
#     def __init__(self):
#
#         pass
#
#     def



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor: editor.Editor

        uic.loadUi('editor/petnetsim.ui', self)
        self.editor.after_init(self)

        self.actionSave.triggered.connect(self.save)
        self.actionSaveAs.triggered.connect(self.save_as)
        self.actionNew.triggered.connect(self.new)
        self.actionOpen.triggered.connect(self.open)

        self.filename = None

    def choose_filename(self):
        self.filename = 'test.pnet.json'

    def new(self):
        self.editor: editor.Editor
        self.editor.clear()

    def open(self):
        self.filename = 'test.pnet.json'
        with open(self.filename, 'r') as f:
            self.editor.load_petrinet(f)

    def save_as(self):
        self.editor: editor.Editor
        if self.editor.verify_petrinet(inform_success=False):
            self.choose_filename()
            self.save_petrinet()

    def save(self):
        self.editor: editor.Editor
        if self.editor.verify_petrinet(inform_success=False):
            if self.filename is None:
                self.choose_filename()
            self.save_petrinet()

    def save_petrinet(self):
        self.editor: editor.Editor
        with open(self.filename, 'w') as f:
            self.editor.save_petrinet(f)


def run():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    app.exec()


if __name__ == '__main__':
    run()
