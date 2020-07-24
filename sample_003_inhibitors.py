from itertools import count, combinations
from petnetsim import *
from random import choice
import numpy as np


A = Place('A', init_tokens=2)
B = Place('B', init_tokens=5)
C = Place('C')
D = Place('D')

places = [A, B, C, D]

T1 = Transition('T1')
T2 = Transition('T2')

transitions = [T1, T2]

arcs = [Arc(A, T1, 1),
        Inhibitor(B, T1, 1),
        Arc(T1, C, 1),
        Arc(B, T2, 1),
        Arc(T2, D, 1),
        ]


def print_sim(step, t):
    print('step:', step, '  t:', t)
    for p in places:
        print(p.name, p.tokens, sep=': ')


# TODO: make into PetriNet object

def run():

    print('------------------------------------')
    print(' run')

    for t in transitions:
        t.reset()
    for p in places:
        p.reset()

    max_steps = 100
    sim_t = 0.0

    print_sim(0, sim_t)

    conflict_groups, conflict_groups_types = make_conflict_groups(transitions)

    # conflig group types


    # masks
    enabled = np.zeros(len(transitions), dtype=np.bool)
    conflict_groups_mask = np.zeros((len(conflict_groups), len(transitions)), dtype=np.bool)
    enabled_conflict_groups = np.zeros((len(conflict_groups), len(transitions)), dtype=np.bool)
    for cgi, cg in enumerate(conflict_groups):
        for ti, t in enumerate(transitions):
            conflict_groups_mask[cgi, ti] = t in cg

    for step in range(1, max_steps):

        # enabled transitions
        for ti, t in enumerate(transitions):
            enabled[ti] = t.enabled()

        if enabled.any():
            np.bitwise_and(enabled, conflict_groups_mask, out=enabled_conflict_groups)

            for cgi, ecg in enumerate(enabled_conflict_groups):
                if ecg.any():
                    t_idx = choice(np.argwhere(ecg))[0]
                    t = transitions[t_idx]
                    t.fire()
                    print(' ', t.name, 'fired')

        # TODO: if no transitions are active, advance time
        num_waiting = 0

        print_sim(step, sim_t)

        if not enabled.any() and num_waiting == 0:
            print(' -- breaking condition --')
            break

    print('transitions stats')
    for t in transitions:
        print(t.name, t.fired_times, sep=': ')


run()
