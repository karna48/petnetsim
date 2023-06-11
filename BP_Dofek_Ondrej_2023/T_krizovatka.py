# doc/drawing/sample_003_inhibitors.svg

from petnetsim import *
from petnetsim import PetriNet
from petnetsim.elements import *
from petnetsim.json_io import loads, dumps
from pprint import pprint
from itertools import chain
import json


def run():
    j = Place('j')
    jv = Place('jv')
    jz = Place('jz')
    oj = Place('oj')

    v = Place('v')
    vz = Place('vz')
    vj = Place('vj')
    ov = Place('ov')

    z = Place('z')
    zv = Place('zv')
    zj = Place('zj')
    oz = Place('oz')



    places = [
              j, jv, jz, oj, v, vj, vz, ov, z, zj, zv, oz]


    JV = TransitionStochastic('JV', 0.7)
    JZ = TransitionStochastic('JZ', 0.3)
    OJZ = TransitionTimed('OJZ', 5)
    OJV = TransitionTimed('OJV', 5)

    VZ = TransitionStochastic('VZ', 0.5)
    VJ = TransitionStochastic('VJ', 0.5)
    OVJ = TransitionTimed('OVJ', 5)
    OVZ = TransitionTimed('OVZ', 5)

    ZJ = TransitionStochastic('ZJ', 0.2)
    ZV = TransitionStochastic('ZV', 0.8)
    OZV = TransitionTimed('OZV', 5)
    OZJ = TransitionTimed('OZJ', 5)

    J = TransitionTimed('J', 1)
    V = TransitionTimed('V', 1)
    Z = TransitionTimed('Z', 1)

    transitions = [
                   JV, JZ, OJZ, OJV, VZ, VJ, OVZ, OVJ, ZV, ZJ, OZJ, OZV, J, V, Z]
    arcs = [Arc(J, j),
            Arc(Z, z),
            Arc(V, v),






            Arc(j, JV),
            Arc(j, JZ),
            Arc(JV, jv),
            Arc(JZ, jz),
            Arc(jz, OJZ),
            Arc(jv, OJV),
            Arc(OJV, ov),
            Arc(OVZ, oz),

            Arc(v, VZ),
            Arc(v, VJ),
            Arc(VZ, vz),
            Arc(VJ, vj),
            Arc(vz, OVZ),
            Arc(vj, OVJ),
            Arc(OVJ, oj),
            Arc(OVZ, vz),

            Arc(z, ZJ),
            Arc(z, ZV),
            Arc(ZJ, zj),
            Arc(ZV, zv),
            Arc(zv, OZV),
            Arc(zj, OZJ),
            Arc(OZJ, oj),
            Arc(OZV, ov),


            Inhibitor(j, OVZ),
            Inhibitor(z, OJV),
            Inhibitor(v, OZJ)


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





    jt = J.fired_times
    vt = V.fired_times
    zt = Z.fired_times
    ojt = oj.tokens
    ovt = ov.tokens
    ozt = oz.tokens
    print('chtelo projet', jt, 'a projelo', ojt)
    print('chtelo projet', vt, 'a projelo', ovt)
    print('chtelo projet', zt, 'a projelo', ozt)

    petri_net_dump = dumps(petri_net.places, petri_net.transitions, petri_net.arcs)
    print(petri_net_dump)
    print('-----------------------------------------------')
    with open('T_kriz.json', 'w') as sem:
        sem.write(petri_net_dump)

    for t in places:
        print(t.name, t.tokens, sep=': ')




run()



