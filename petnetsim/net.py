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

        self._dot_T = {}

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



    def validate(self):
        # transitions with priority and stochastic cannot share inputs
        self._construct_inputs()



        raise ValueError('xxx')
