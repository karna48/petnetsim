
# doc/drawing/sample_001_basic.svg

from petnetsim import *


def run():
    empty_net = PetriNet([], [], [])
    while not empty_net.ended and empty_net.step_num < 1000:
        empty_net.step()

    petri_net = PetriNet([Place('A', init_tokens=6),
                          Place('B', init_tokens=4),
                          Place('C'),
                          Place('D')],
                         [Transition('T')],
                         [Arc('A', 'T', 2),
                          Arc('B', 'T', 1),
                          Arc('T', 'C', 4),
                          Arc('T', 'D', 1)])

    print('------------------------------------')
    print(' run')

    petri_net.reset()

    max_steps = 100

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

run()
