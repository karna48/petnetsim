from PyQt5.QtCore import QTimer
from . import Editor
from petnetsim import PetriNet
from petnetsim.elements import TransitionTimed
from time import time
from itertools import chain


class SimulationController:
    def __init__(self, main_window, editor: Editor):
        self.main_window = main_window
        self.editor = editor
        self.petrinet = PetriNet((), (), ())  # empty net, will be replaced
        self.step_animation_duration = 0
        self.t1 = time()  # beginning of current step
        self.auto_run_next_step = False
        self.step_fired_arcs = []

        self.animate_timer = QTimer()
        self.animate_timer.timeout.connect(self.animate)
        self.animate_waiting = True  # timer is running, but no animation and stepping should be done now

    def init_petrinet(self):
        self.petrinet = self.editor.verified_petrinet(inform_success=False, include_item_lookups=True)
        self.reset()

    def reset(self):
        self.petrinet.reset()
        self.step_fired_arcs.clear()
        self.auto_run_next_step = False
        self.animate_waiting = True
        for place_item in self.petrinet.place_item_lookup.values():
            place_item.update_tokens_text_simulation()

        for transition_item in self.petrinet.transition_item_lookup.values():
            transition_item.set_brush(False)

        for arc_item in self.petrinet.arc_item_lookup.values():
            arc_item.fired_marker_set_visibility(False)

    def run(self):
        self.auto_run_next_step = True
        self.step()

    def step(self):
        self.animate_waiting = False
        # check every step if user changed simulation speed
        self.step_animation_duration = self.main_window.simulation_wait_doubleSpinBox.value()
        self.t1 = time()

        if self.step_animation_duration > 0:
            for t in self.petrinet.fired:
                self.petrinet.transition_item_lookup[t].set_brush(False)

        if not self.petrinet.ended:
            self.petrinet.step()
            print('step:', self.petrinet.step_num,
                  't:', self.petrinet.time,
                  'fired:', ', '.join(t.name for t in self.petrinet.fired))
            self.petrinet.print_places()
        else:
            self.auto_run_next_step = False
            self.animate_waiting = True

        if self.step_animation_duration > 0:
            for arc in self.step_fired_arcs:
                self.petrinet.arc_item_lookup[arc].fired_marker_set_visibility(False)

            self.step_fired_arcs.clear()
            self.step_fired_arcs.extend(
                chain.from_iterable(t.in_arcs if isinstance(t, TransitionTimed) else chain(t.in_arcs, t.outputs)
                                    for t in self.petrinet.fired)
            )
            self.step_fired_arcs.extend(chain.from_iterable(t.outputs for t in self.petrinet.fired_phase2))
            for arc in self.step_fired_arcs:
                self.petrinet.arc_item_lookup[arc].fired_marker_set_visibility(True)

            for t in chain(self.petrinet.fired, self.petrinet.fired_phase2):
                for place in chain((pt_arc.source for pt_arc in t.in_arcs), (tp_arc.target for tp_arc in t.outputs)):
                    self.petrinet.place_item_lookup[place].update_tokens_text_simulation()

            for t in self.petrinet.fired:
                self.petrinet.transition_item_lookup[t].set_brush(True)

    @property
    def step_number(self):
        return self.petrinet.step_num

    @property
    def time(self):
        return self.petrinet.time

    def animate(self):
        if not self.animate_waiting:
            if self.step_animation_duration > 0:
                t2 = time()
                dt = t2-self.t1
                tpol = min(dt, self.step_animation_duration) / self.step_animation_duration  # interpolation coefficient
                for arc in self.step_fired_arcs:
                    self.petrinet.arc_item_lookup[arc].fired_marker_interpolate_position(tpol)
                can_auto_next_step = self.auto_run_next_step and dt >= self.step_animation_duration  # deny auto next step
            else:
                can_auto_next_step = self.auto_run_next_step

            if can_auto_next_step:
                self.step()
