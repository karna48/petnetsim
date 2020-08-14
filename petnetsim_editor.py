from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
import editor
from editor.mode import ModeSwitch, Mode


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mode_switch = ModeSwitch(self)

        uic.loadUi('editor/petnetsim.ui', self)

        self.item_properties.item_selected(None)

        self.actionSave.triggered.connect(self.save)
        self.actionSaveAs.triggered.connect(self.save_as)
        self.actionNew.triggered.connect(self.new)
        self.actionOpen.triggered.connect(self.open)

        self.filename = None

        self.open()  # TODO remove

    @property
    def mode(self):
        return self.mode_switch.mode

    @mode.setter
    def mode(self, new_mode):
        self.mode_switch.mode = new_mode

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
        if self.editor.verified_petrinet(inform_success=False) is not None:
            self.choose_filename()
            self.save_petrinet()

    def save(self):
        self.editor: editor.Editor
        if self.editor.verified_petrinet(inform_success=False) is not None:
            if self.filename is None:
                self.choose_filename()
            self.save_petrinet()

    def save_petrinet(self):
        self.editor: editor.Editor
        with open(self.filename, 'w') as f:
            self.editor.save_petrinet(f)

    def simulation_editor_switched(self, is_simulation):
        self.mode = Mode.Simulation if is_simulation else Mode.Normal

    def sim_buttons_enabled(self, enabled):
        sim_buttons = (self.simulation_run_pushButton,
                       self.simulation_step_pushButton,
                       self.simulation_reset_pushButton)
        for sb in sim_buttons:
            sb.setEnabled(enabled)


def run():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    app.exec()


if __name__ == '__main__':
    run()
