from itertools import count, combinations
from petnetsim import *

def run():
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

    petri_net.print_places()

    while not petri_net.ended and petri_net.step_num < max_steps:
        print('--------------- step', petri_net.step_num)
        petri_net.step()
        petri_net.print_places()

    if petri_net.ended:
        print('  breaking condition')
    else:
        print('  max steps reached')

run()
