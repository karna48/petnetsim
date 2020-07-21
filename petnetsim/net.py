# import itertools
# from collections import defaultdict
# from .elements import *
#
#
# class PetriNet:
#     def __init__(self):
#         self.P = []  # places
#         self.T = []  # transitions
#         self.A = []  # arcs
#         self.I = []  # inhibitor arcs
#
#         self.dot_T = defaultdict(list)  # transition - input places
#         self.T_dot = defaultdict(list)  # transition - output places
#         self.W = defaultdict(lambda: 0)  # weights lookup
#
#     def reset(self):
#         for obj in itertools.chain(self.P, self.T, self.A, self.I):
#             obj.reset()
#         self._construct_inputs()
#
#     def step(self):
#         pass
#
#     def _fill_W(self):
#         # weight matrix
#         for p, t in itertools.product(self.P, self.T):
#             pass
#
#     def _construct_inputs(self):
#         self.dot_T.clear()
#
#         for arc in self.A:
#             if isinstance(arc.target, Transition):
#                 self.dot_T[arc.target].append(arc.source)
#
#             if isinstance(arc.source, Transition):
#                 self.T_dot[arc.source].append(arc.target)
#
#     def validate(self):
#         # transitions with priority and stochastic cannot share inputs
#         self._construct_inputs()
#         # TODO: is this right?
#         for target_place, source_transitions in self.dot_T.items():
#
#             source_T_types = [type(st) for st in source_transitions]
#             #sum()
#             if int(TransitionPriority in source_T_types) > 1:
#                 raise ValueError('place :"'+str(target_place.name)+'" has incompatibile source transitions')
#
#
#         #raise ValueError('xxx')
