# doc/drawing/sample_005_priority.svg

from petnetsim import *


def run():

    arc_defs = [('Z', 'T'+str(i)) for i in range(1, 8)] + \
               [('T' + str(i), chr(j+ord('A'))) for i, j in zip(range(1, 8), range(0, 7))]

    petri_net = PetriNet([Place('Z', init_tokens=25),
                          'A',
                          'B',
                          'C',
                          Place('D', capacity=3),
                          Place('E', capacity=3),
                          Place('F', capacity=3),
                          Place('G', capacity=3)],
                         ['T1',
                          TransitionPriority('T2', 0),
                          TransitionPriority('T3', 0),
                          TransitionPriority('T4', 1),
                          TransitionPriority('T5', 1),
                          TransitionPriority('T6', 2),
                          TransitionPriority('T7', 2)],
                         arc_defs)

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
