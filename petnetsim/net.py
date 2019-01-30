import itertools

from .xml_loader import load_xml


class PetriNet:
    def __init__(self):
        self.P = []  # places
        self.T = []  # transitions
        self.A = []  # arcs
        self.I = []  # inhibitor arcs

        # used during actual simulation
        self._T_normal = None
        self._T_priority = None
        self._T_timed = None
        self._T_stochastic = None

    def reset(self):
        for obj in itertools.chain(self.P, self.T, self.A, self.I):
            obj.reset()
        self._construct_inputs()

    def step(self):
        pass

    def _construct_inputs(self):
        for a in self.A:
            a.target


    def validate(self):
        # transitions with priority and stochastic cannot share inputs
        raise ValueError('xxx')
