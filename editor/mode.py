import enum


class Mode(enum.IntEnum):
    Normal = 0
    ArcSource = 1
    ArcTarget = 2
    Simulation = 100


ModeStrings = {Mode.Normal: 'Editor: Normal',
               Mode.ArcSource: 'Editor: Arc source',
               Mode.ArcTarget: 'Editor: Arc target',
               Mode.Simulation: 'Simulation',
               }


class ModeSwitch:
    def __init__(self, main_window):
        from .simulationcontroller import SimulationController  # avoid circular dependency

        self._mode = Mode.Normal
        self.main_window = main_window
        self.simulation_controller: SimulationController = main_window.simulation_controller

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        old_mode = self.mode
        editor = self.main_window.editor
        # cleanup modes
        arc_modes = (Mode.ArcSource, Mode.ArcTarget)
        if new_mode not in arc_modes and old_mode in arc_modes:
            editor.cancel_arc_modes()

        # actual change
        self._mode = new_mode
        self.main_window.mode_label.setText(ModeStrings[self._mode])

        if self.mode == Mode.Normal:
            self.main_window.item_properties.edits_enabled(True)
            self.main_window.sim_buttons_enabled(False)

        if self.mode == Mode.Simulation:
            self.main_window.item_properties.edits_enabled(False)
            self.main_window.sim_buttons_enabled(True)
            self.simulation_controller.init_petrinet()
            self.simulation_controller.reset()
            self.simulation_controller.animate_timer.start(0)

        if self.mode != Mode.Simulation and old_mode == Mode.Simulation:
            self.simulation_controller.reset()
            self.simulation_controller.animate_timer.stop()
            self.main_window.editor.update_all_texts()