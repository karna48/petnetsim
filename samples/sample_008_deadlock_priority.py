# doc/drawing/sample_008_deadlock_priority.svg

from itertools import count, combinations
from petnetsim import *
import numpy as np
import itertools

def run():

    resource_places = [Place('R1', 1), Place('R2', 1)]
    process_states = [Place(p+'CriticalSectionIn', 1) for p in ['P1', 'P2']] + \
                     ['P1HaveR1', 'P2HaveR2'] + \
                     [p+s for p, s in itertools.product(['P1', 'P2'], ['Processing', 'CriticalSectionOut'])]
    transitions = [p+s for p, s in itertools.product(['P1', 'P2'], ['Release'])] + \
                  [TransitionPriority('P1AquireR1', 1), TransitionPriority('P2AquireR2', 1), TransitionPriority('P1AquireR2', 1), TransitionPriority('P2AquireR1', 1),
                   'P1ReleaseR1Retry', 'P2ReleaseR2Retry']
    arcs = [('R1', 'P1AquireR1'), ('R1', 'P2AquireR1'), ('R2', 'P1AquireR2'), ('R2', 'P2AquireR2'),
            ('P1Release', 'R1'), ('P1Release', 'R2'), ('P2Release', 'R1'), ('P2Release', 'R2'),
            ('P1ReleaseR1Retry', 'P1CriticalSectionIn'), ('P2ReleaseR2Retry', 'P2CriticalSectionIn'),
            ('P1ReleaseR1Retry', 'R1'), ('P2ReleaseR2Retry', 'R2'),
            ('P1HaveR1', 'P1ReleaseR1Retry'), ('P2HaveR2', 'P2ReleaseR2Retry')]

    # chains of arcs
    proc1chain = ['P1CriticalSectionIn', 'P1AquireR1', 'P1HaveR1', 'P1AquireR2', 'P1Processing', 'P1Release', 'P1CriticalSectionOut']
    proc2chain = ['P2CriticalSectionIn', 'P2AquireR2', 'P2HaveR2', 'P2AquireR1', 'P2Processing', 'P2Release', 'P2CriticalSectionOut']

    for pc in [proc1chain, proc2chain]:
        for s, t in zip(pc[:-1], pc[1:]):
            arcs.append((s, t))

    petri_net = PetriNet(resource_places+process_states,
                         transitions,
                         arcs)

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
