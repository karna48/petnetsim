# doc/drawing/sample_003_inhibitors.svg

from petnetsim import *
from petnetsim import PetriNet
from petnetsim.elements import *
from petnetsim.json_io import loads, dumps
from pprint import pprint
from itertools import chain
import json


def run():
    j = Place('j', capacity=1)

    oj = Place('oj', capacity=1)

    v = Place('v', capacity=1)

    ov = Place('ov', capacity=1)

    z = Place('z', capacity=1)

    oz = Place('oz', capacity=1)

    s = Place('s', capacity=1)

    os = Place('os', capacity=1)





    places = [s, v, z, j,
               oj, ov,  oz,  os]




    JS = TransitionTimed('JS', 0.5)



    ZV = TransitionTimed('ZV', 0.5)



    VZ = TransitionTimed('VZ', 0.5)



    SJ = TransitionTimed('SJ', 0.5)




    transitions = [

        JS,
        VZ,
        ZV,
         SJ

        ]
    arcs = [Arc(j,JS),
            Arc(JS,os),
            Arc(s,SJ),
            Arc(SJ,oj),
            Arc(v,VZ),
            Arc(VZ,oz),
            Arc(z,ZV),
            Arc(ZV,ov)
            ]

    petri_net = PetriNet(places, transitions, arcs)
    print('conflict groups:', petri_net.conflict_groups_str)

    print('------------------------------------')
    print(' run')


    petri_net.reset()

    max_steps = 120



    while not petri_net.ended and petri_net.step_num < max_steps:
        petri_net.step()
        print('--------------- step', petri_net.step_num, '   t:', petri_net.time)
        petri_net.print_places()


    if petri_net.ended:
        print('  breaking condition')
    else:
        print('  max steps reached')





    #jt = J.fired_times
    #vt = V.fired_times
    #zt = Z.fired_times
    #st = S.fired_times
    ojt = oj.tokens
    ovt = ov.tokens
    ozt = oz.tokens
    ost = os.tokens
    #print('chtelo projet', jt, 'a projelo v tomto smeru', ojt)
    #print('chtelo projet', vt, 'a projelo v tomto smeru', ovt)
    #print('chtelo projet', zt, 'a projelo v tomto smeru', ozt)
    #print('chtelo projet', st, 'a projelo v tomto smeru', ost)

    petri_net_dump = dumps(petri_net.places, petri_net.transitions, petri_net.arcs)
    print(petri_net_dump)
    print('-----------------------------------------------')
    with open('krizovatky/Silnice.json', 'w') as sem:
        sem.write(petri_net_dump)

    for t in places:
        print(t.name, t.tokens, sep=': ')




run()



