from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys
import editor
from editor.mode import ModeSwitch, Mode
from editor.simulationcontroller import SimulationController
from pathlib import Path

root_path = Path(__file__).parent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str((root_path / 'editor' / 'petnetsim.ui').resolve()), self)
        self.setWindowIcon(QIcon(str((root_path / 'editor' / 'pns_icon.svg').resolve())))

        self.item_properties.after_init()
        self.item_properties.item_selected(None)

        self.actionSave.triggered.connect(self.save)
        self.actionSaveAs.triggered.connect(self.save_as)
        self.actionNew.triggered.connect(self.new)
        self.actionOpen.triggered.connect(self.open)

        self.filename = None

        self.simulation_controller = SimulationController(self, self.editor)
        self.mode_switch = ModeSwitch(self)

    @property
    def mode(self):
        return self.mode_switch.mode

    @mode.setter
    def mode(self, new_mode):
        self.mode_switch.mode = new_mode

    def choose_filename_save(self):
        filename, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption='Select file containing petrinet in JSON',
            directory=self.filename if self.filename is not None else '.json',
            filter='PetriNet in JSON (*.json);;All files (*.*)')
        if len(filename):
            self.filename = filename
        else:
            self.filename = None

    def new(self):
        self.editor: editor.Editor
        self.editor.clear()
        self.filename = None

    def open(self):
        filename, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select file containing petrinet in JSON',
            directory='.',
            filter='PetriNet in JSON (*.json);;All files (*.*)')

        if len(filename) > 0:
            self.filename = filename
            try:
                with open(self.filename, 'r') as f:
                    self.editor.load_petrinet(f)
            except FileNotFoundError:
                print('waring: file not found')

    def save_as(self):
        self.editor: editor.Editor
        if self.editor.verified_petrinet(inform_success=False) is not None:
            self.choose_filename_save()
            if self.filename is not None:
                self.save_petrinet()

    def save(self):
        self.editor: editor.Editor
        if self.editor.verified_petrinet(inform_success=False) is not None:
            if self.filename is None:
                self.choose_filename_save()
            if self.filename is not None:
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

    def simulation_run(self):
        self.simulation_controller.run()

    def simulation_step(self):
        self.simulation_controller.auto_run_next_step = False
        self.simulation_controller.step()

    def simulation_reset(self):
        self.simulation_controller.reset()


def run():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    app.exec()


if __name__ == '__main__':
    run()
