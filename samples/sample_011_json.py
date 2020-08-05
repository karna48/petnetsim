from petnetsim import PetriNet
from petnetsim.elements import *
from petnetsim.json_io import loads, dumps
from pprint import pprint
import json

ctx = new_context()

unnamed_place_1 = Place(init_tokens=5, context=ctx)
unnamed_place_2 = Place(init_tokens=10, context=ctx)
unnamed_place_3 = Place(init_tokens=5, context=ctx)
unnamed_place_4 = Place(init_tokens=3, context=ctx)
unnamed_place_5 = Place(context=ctx)
unnamed_place_6 = Place(context=ctx)

unnamed_transition_1 = TransitionPriority(name=None, priority=1, context=ctx)
unnamed_transition_2 = TransitionPriority(name=None, priority=2, context=ctx)
unnamed_transition_3 = TransitionStochastic(name=None, probability=0.7, context=ctx)
unnamed_transition_4 = TransitionTimed(name=None, t_min=2, context=ctx)
unnamed_transition_5 = TransitionTimed(name=None, t_min=1, t_max=3, p_distribution_func=uniform_distribution, context=ctx)
unnamed_transition_6 = Transition(name=None, context=ctx)
unnamed_transition_7 = Transition(name=None, context=ctx)

petri_net = \
    PetriNet(
        (Place('A', 8, context=ctx), Place('B', capacity=6, context=ctx),
         Place('C', 10, context=ctx), Place('D', capacity=5, context=ctx), 'E',
         unnamed_place_1, 'F', 'G', unnamed_place_2, unnamed_place_5, unnamed_place_6,
         unnamed_place_3, unnamed_place_4, 'H', 'I'),
        ('T1', unnamed_transition_1, unnamed_transition_2,
         TransitionStochastic('TX', 0.3, context=ctx),
         unnamed_transition_3, unnamed_transition_4,
         unnamed_transition_5, unnamed_transition_6,
         unnamed_transition_7),
        (('A', 'T1'), ('T1', 'B', 3), ('C', unnamed_transition_1, 2), ('C', unnamed_transition_2),
         (unnamed_transition_1, 'D'), (unnamed_transition_2, 'E'),
         (unnamed_place_1, 'TX'), (unnamed_place_1, unnamed_transition_3),
         ('TX', 'F'), (unnamed_transition_3, 'F'), (unnamed_transition_3, 'G'),
         (unnamed_place_2, unnamed_transition_4), (unnamed_place_2, unnamed_transition_5),
         (unnamed_transition_4, unnamed_place_5), (unnamed_transition_5, unnamed_place_6),
         (unnamed_place_3, unnamed_transition_6, 3), (unnamed_transition_6, 'H'),
         Inhibitor(unnamed_place_3, unnamed_transition_7, context=ctx),
         (unnamed_place_4, unnamed_transition_7), (unnamed_transition_7, 'I')),
        context=ctx)

petri_net_dump = dumps(petri_net.places, petri_net.transitions, petri_net.arcs)

data = json.loads(petri_net_dump)
data['places'] = {int(k): v for k, v in data['places'].items()}
data['transitions'] = {int(k): v for k, v in data['transitions'].items()}
data['arcs'] = {int(k): v for k, v in data['arcs'].items()}
print('petri_net_dump (edited):')
pprint(data, indent=4, compact=True, width=200)

ctx2 = new_context()

p2_places, p2_transitions, p2_arcs = loads(petri_net_dump, ctx2)

petri_net_from_dump = PetriNet(p2_places, p2_transitions, p2_arcs)

print('petri_net_from_dump')
petri_net_from_dump.print_all()


def compare_petri_nets(pn1, pn2):
    diff = []


diff = compare_petri_nets(petri_net, petri_net_from_dump)

print('differences in nets:')
pprint(diff)