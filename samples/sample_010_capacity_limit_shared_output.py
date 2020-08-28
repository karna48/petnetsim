# doc/drawing/sample_010_capacity_limit_shared.svg

from itertools import count, combinations
from petnetsim import *
import numpy as np
import itertools

def run():

    petri_net = PetriNet([Place('X', 5), Place('Y', capacity=10), Place('Z', capacity=100), Place('P', 5), Place('Q', capacity=15), Place('R', 5), Place('S', 16)],
                         [chr(c) for c in range(ord('A'), ord('G')+1)],
                         [('X', 'A'), ('A', 'Y'), ('B', 'Y'), ('Y', 'E'), ('E', 'Z'), ('F', 'Z'), ('S', 'F'),
                          ('P', 'B'), ('P', 'C'), ('P', 'D'), ('C', 'Q'), ('D', 'Q'), ('G', 'Q'), ('R', 'G')])

    print('conflict groups:', [sorted([t.name for t in cg]) for cg in petri_net.conflict_groups_sets])

    print('------------------------------------')
    print(' run')

    petri_net.reset()

    max_steps = 100

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
        print('  -- breaking condition --')
    else:
        print(' -- max steps reached --')

    print('transitions stats')
    for t in petri_net.transitions:
        print('  '+t.name, t.fired_times, sep=': ')


run()
