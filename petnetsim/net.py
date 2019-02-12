import itertools

from .xml_loader import load_xml


class PetriNet:
    def __init__(self):
        self.P = []  # places
        self.T = []  # transitions
        self.A = []  # arcs
        self.I = []  # inhibitor arcs

        # used during actual simulation
        self._T_normal = []
        self._T_priority = []
        self._T_timed = []
        self._T_stochastic = []

        self._dot_T = {}  #
        self._T_dot = {}

    def reset(self):
        for obj in itertools.chain(self.P, self.T, self.A, self.I):
            obj.reset()
        self._construct_inputs()

    def step(self):
        pass

    def _construct_inputs(self):
        from . import Transition
        self._dot_T.clear()

        for arc in self.A:
            if isinstance(arc.target, Transition):
                self._dot_T[arc.target].append(arc.source)

            if isinstance(arc.source, Transition):
                self._T_dot[arc.source].append(arc.target)

    def validate(self):
        # transitions with priority and stochastic cannot share inputs
        self._construct_inputs()
        for target, source_transitions in self._dot_T
            source_T_types = [type(st) for st in source_transitions]


        raise ValueError('xxx')
