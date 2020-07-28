# doc/drawing/sample_004_stochastic.svg

from itertools import count, combinations
from petnetsim import *
import numpy as np


def run():
    petri_net = PetriNet([Place('Z', init_tokens=10000), Place('A'), Place('B')],
                         [TransitionStochastic('T30', 0.3), TransitionStochastic('T70', 0.7)],
                         [Arc('Z', 'T30'), Arc('Z', 'T70'), Arc('T30', 'A'), Arc('T70', 'B')])

    print('------------------------------------')
    print(' run')


    petri_net.reset()

    max_steps = 100000

    print('--------------- step', petri_net.step_num)
    petri_net.print_places()

    while not petri_net.ended and petri_net.step_num < max_steps:
        petri_net.step()
        print('--------------- step', petri_net.step_num)
        petri_net.print_places()

    if petri_net.ended:
        print('  breaking condition')
    else:
        print('  max steps reached')

    print('transitions stats')
    for t in petri_net.transitions:
        print(t.name, t.fired_times, sep=': ')


run()
