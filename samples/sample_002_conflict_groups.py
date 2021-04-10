# doc/drawing/sample_002_conflict_groups.svg

from petnetsim import *

def run():
    petri_net = PetriNet([Place('A', init_tokens=10),
                          Place('B', capacity=2),
                          'C'],
                         ['T1', 'T2', 'T3', 'T4', 'T5'],
                         [('A', 'T1'), ('A', 'T2'), ('A', 'T3'),
                          ('T1', 'C'), ('T2', 'C'), ('T3', 'B'),
                          ('T4', 'B'), ('B', 'T5'), ('C', 'T5')]
                         )

    print('------------------------------------')
    print(' run')

    petri_net.reset()

    max_steps = 100

    print('conflict groups:', petri_net.conflict_groups_str)

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
