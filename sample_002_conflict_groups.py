from itertools import count, combinations
from petnetsim.elements import Place, Arc, Transition
from random import choice
import numpy as np


A = Place('A', init_tokens=10)
B = Place('B', capacity=2)
C = Place('C')

places = [A, B, C]

T1 = Transition('T1')
T2 = Transition('T2')
T3 = Transition('T3')
T4 = Transition('T4')
T5 = Transition('T5')

transitions = [T1, T2, T3, T4, T5]

arcs = [Arc(A, T1, 1),
        Arc(A, T2, 1),
        Arc(A, T3, 1),
        Arc(T1, C, 1),
        Arc(T2, C, 1),
        Arc(T3, B, 1),
        Arc(T4, B, 1),
        Arc(B, T5, 1),
        Arc(C, T5, 1),
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

    conflict_groups = [{transitions[0]}]
    for t in transitions[1:]:
        add_to_cg = False
        # print('t: ', t.name)
        for cg in conflict_groups:
            for cg_t in cg:
                t_in = set(arc.source for arc in t.inputs)
                t_out = set(arc.target for arc in t.outputs)
                cg_t_in = set(arc.source for arc in cg_t.inputs)
                cg_t_out = set(arc.target for arc in cg_t.outputs)
                # print(' cg_t: ', cg_t.name)
                # print('   t_in:', [i.name for i in t_in])
                # print('   cg_t_in:', [i.name for i in cg_t_in])
                # print('   t_out:', [i.name for i in t_out])
                # print('   cg_t_out:', [i.name for i in cg_t_out])

                add_to_cg = add_to_cg or not t_in.isdisjoint(cg_t_in)
                add_to_cg = add_to_cg or not t_out.isdisjoint(cg_t_out)
                if add_to_cg:
                    break
            if add_to_cg:
                cg.add(t)
                break

        #print(' add_to_cg', add_to_cg)

        if not add_to_cg:
            conflict_groups.append([t])

    print('conflict groups:', [sorted([t.name for t in cg]) for cg in conflict_groups])

    # masks
    enabled = np.zeros(len(transitions), dtype=np.bool)
    conflict_groups_mask = np.zeros((len(conflict_groups), len(transitions)), dtype=np.bool)
    enabled_conflict_groups = np.zeros((len(conflict_groups), len(transitions)), dtype=np.bool)
    for cgi, cg in enumerate(conflict_groups):
        for ti, t in enumerate(transitions):
            conflict_groups_mask[cgi, ti] = t in cg

    print('conflict_groups_mask')
    print(conflict_groups_mask)

    for step in range(1, max_steps):

        # enabled transitions
        for ti, t in enumerate(transitions):
            enabled[ti] = t.enabled()

        if enabled.any():
            np.bitwise_and(enabled, conflict_groups_mask, out=enabled_conflict_groups)

            for cgi, ecg in enumerate(enabled_conflict_groups):
                if ecg.any():
                    t_idx = choice(np.argwhere(ecg))[0]
                    transitions[t_idx].fire()

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
