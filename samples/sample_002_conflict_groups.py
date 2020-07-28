# doc/drawing/sample_002_conflict_groups.svg

from itertools import count, combinations
from petnetsim import *
from random import choice
import numpy as np

def run():
    petri_net = PetriNet([Place('A', init_tokens=10),
                          Place('B', capacity=2),
                          Place('C')],
                         [Transition('T1'), Transition('T2'), Transition('T3'), Transition('T4'), Transition('T5')],
                         [Arc('A', 'T1', 1),
                          Arc('A', 'T2', 1),
                          Arc('A', 'T3', 1),
                          Arc('T1', 'C', 1),
                          Arc('T2', 'C', 1),
                          Arc('T3', 'B', 1),
                          Arc('T4', 'B', 1),
                          Arc('B', 'T5', 1),
                          Arc('C', 'T5', 1),]
                         )

    print('------------------------------------')
    print(' run')

    petri_net.reset()

    max_steps = 100

    print('conflict groups:', [sorted([t.name for t in cg]) for cg in petri_net.conflict_groups_sets])

    print('--------------- step', petri_net.step_num)
    petri_net.print_places()

    while not petri_net.ended and petri_net.step_num < max_steps:
        petri_net.step()
        print('--------------- step', petri_net.step_num)

        if len(petri_net.fired):
            print(' fired: ', end='')
            print(*(t.name for t in petri_net.fired), sep=', ')
        petri_net.print_places()

    if petri_net.ended:
        print('  breaking condition')
    else:
        print('  max steps reached')

    print('transitions stats')
    for t in petri_net.transitions:
        print(t.name, t.fired_times, sep=': ')

run()
