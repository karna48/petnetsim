from petnetsim import PetriNet, Place, Transition, new_context
import petnetsim.json_io


def run():
    subnet_ctx = new_context()
    with open('sample_012_netclone.json') as f:
        sn_places, sn_transitions, sn_arcs, sn_graphics = petnetsim.json_io.load(f, subnet_ctx)
        subnet = PetriNet(sn_places, sn_transitions, sn_arcs, subnet_ctx)

    places = [Place('Waves', 10)]
    transitions = [Transition('make_wave')]
    arcs = [('Waves', 'make_wave')]

    for client_i in range(1, 11):
        prefix = f'Client_{client_i}_'
        subnet.clone(prefix, places, transitions, arcs)
        arcs.append(('Waves', prefix + 'Input'))

    petri_net = PetriNet(places, transitions, arcs)
    print('conflict groups:', petri_net.conflict_groups_str)

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

    print('--- transitions stats -------------------------')
    for t in transitions:
        print(t.name, t.fired_times, sep=': ')

run()
