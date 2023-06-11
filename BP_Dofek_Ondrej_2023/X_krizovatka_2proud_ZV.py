from petnetsim import *
from petnetsim import PetriNet
from petnetsim.elements import *
from petnetsim.json_io import loads, dumps
from pprint import pprint
from itertools import chain
import json

def run():
    cervena1 = Place('cervenaZV', init_tokens=1)
    zelena1 = Place('zelenaZV')
    cervena2 = Place('cervenaSJ')
    zelena2 = Place('zelenaSJ', init_tokens=1)
    sem1 = Place('sem1')
    sem2 = Place('sem2')
    oranzova1 = Place('oranzova1')
    oranzova2 = Place('oranzova2')

    j = Place('j', capacity=10)
    rj = Place('rj')
    jv = Place('jv')
    jz = Place('jz')
    js = Place('js')
    ojz = Place('ojz')
    ojv = Place('ojv')
    ojs = Place('ojs')
    oj = Place('oj', capacity=1)
    pj = Place('pj', capacity=1)

    v = Place('v', capacity=10)
    rv = Place('rv')
    vz = Place('vz')
    vj = Place('vj')
    vs = Place('vs')
    ovz = Place('ovz')
    ovj = Place('ovj')
    ovs = Place('ovs')
    ov = Place('ov', capacity=1)
    pv = Place('pv', capacity=2)

    z = Place('z', capacity=10)
    rz = Place('rz')
    zv = Place('zv')
    zj = Place('zj')
    zs = Place('zs')
    ozj = Place('ozj')
    ozv = Place('ozv')
    ozs = Place('ozs')
    oz = Place('oz', capacity=1)
    pz = Place('pz', capacity=2)

    s = Place('s', capacity=10)
    rs = Place('rs')
    sv = Place('sv')
    sj = Place('sj')
    sz = Place('sz')
    osz = Place('osz')
    osv = Place('osv')
    osj = Place('osj')
    os = Place('os', capacity=1)
    ps = Place('ps', capacity=1)

    places = [cervena1, zelena1, cervena2, zelena2, sem1, sem2, oranzova1, oranzova2,
              s, v, z, j, ojs, ojv, ojz, osv, osz, osj, ovz, ovs, ovj, ozv, ozs, ozj,
              rj, jv, jz, js, oj, rv, vj, vs, vz, ov, rz, zj, zs, zv, oz, rs, sj, sv, sz, os, ps, pj, pz, pv
              ]

    T1 = TransitionTimed('T1', 20)
    T2 = TransitionTimed('T2', 20)
    T3 = TransitionTimed('T3', 20)
    T4 = TransitionTimed('T4', 20)
    T5 = TransitionTimed('T5', 2)
    T6 = TransitionTimed('T6', 2)

    RJ = Transition('RJ')
    JV = TransitionStochastic('JV', 0.25)
    JZ = TransitionStochastic('JZ', 0.25)
    JS = TransitionStochastic('JS', 0.5)
    OJZ = TransitionTimed('OJZ', 2)
    OJV = TransitionTimed('OJV', 2)
    OJS = TransitionTimed('OJS', 2)
    OJZ1 = Transition('OJZ1')
    OJV1 = Transition('OJV1')
    OJS1 = Transition('OJS1')

    RV = Transition('RV')
    VZ = TransitionStochastic('VZ', 0.5)
    VJ = TransitionStochastic('VJ', 0.25)
    VS = TransitionStochastic('VS', 0.25)
    OVS = TransitionTimed('OVS', 2)
    OVJ = TransitionTimed('OVJ', 2)
    OVZ = TransitionTimed('OVZ', 2)
    OVZ1 = Transition('OVZ1')
    OVJ1 = Transition('OVJ1')
    OVS1 = Transition('OVS1')

    RZ = Transition('RZ')
    ZJ = TransitionStochastic('ZJ', 0.25)
    ZV = TransitionStochastic('ZV', 0.25)
    ZS = TransitionStochastic('ZS', 0.5)
    OZV = TransitionTimed('OZV', 2)
    OZJ = TransitionTimed('OZJ', 2)
    OZS = TransitionTimed('OZS', 2)
    OZV1 = Transition('OZV1')
    OZJ1 = Transition('OZJ1')
    OZS1 = Transition('OZS1')

    RS = Transition('RS')
    SJ = TransitionStochastic('SJ', 0.5)
    SV = TransitionStochastic('SV', 0.25)
    SZ = TransitionStochastic('SZ', 0.25)
    OSV = TransitionTimed('OSV', 2)
    OSZ = TransitionTimed('OSZ', 2)
    OSJ = TransitionTimed('OSJ', 2)
    OSZ1 = Transition('OSZ1')
    OSJ1 = Transition('OSJ1')
    OSV1 = Transition('OSV1')

    #J = TransitionTimed('J', 1)
    #V = TransitionTimed('V', 1)
    #Z = TransitionTimed('Z', 1)
    #S = TransitionTimed('S', 1)

    transitions = [T1, T2, T3, T4, T5, T6, RV, RJ, RZ, RS,
        JV, JZ, JS, OJZ, OJV, OJS, OJZ1, OJV1, OJS1,
        VZ, VJ, VS, OVZ, OVJ, OVS, OVZ1, OVJ1, OVS1,
        ZV, ZJ, ZS, OZJ, OZV, OZS, OZJ1, OZV1, OZS1,
        SV, SJ, SZ, OSV, OSJ, OSZ, OSV1, OSJ1, OSZ1

       # ,J, S, V, Z
                   ]

    arcs = [Arc(cervena1, T1), Arc(T1,zelena1), Arc(zelena1,T2), Arc(T2, cervena1),
        Arc(cervena2, T3), Arc(T3, zelena2), Arc(zelena2, T4), Arc(T4, cervena2),
            Arc(T2, oranzova1), Arc(oranzova1, T5), Arc(T5, sem1), Arc(sem1, T3),
            Arc(T4, oranzova2), Arc(oranzova2, T6), Arc(T6, sem2), Arc(sem2, T1),



            #Arc(J, j),
            #Arc(Z, z),
            #Arc(V, v),
            #Arc(S, s),


            #Arc(J, j),
            #Arc(Z, z),
            #Arc(V, v),
            #Arc(S, s),
            Arc(j, RJ),
            Arc(z, RZ),
            Arc(v, RV),
            Arc(s, RS),
            Arc(RJ, rj),
            Arc(RZ, rz),
            Arc(RV, rv),
            Arc(RS, rs),
            Arc(RJ, pj),
            Arc(RS, ps),
            Arc(RV, pv),
            Arc(RZ, pz),

            Arc(rj, JV),
            Arc(rj, JZ),
            Arc(rj, JS),
            Arc(JV, jv),
            Arc(JZ, jz),
            Arc(JS, js),
            Arc(jz, OJZ),
            Arc(jv, OJV),
            Arc(js, OJS),
            Arc(OJV, ojv),
            Arc(OJZ, ojz),
            Arc(OJS, ojs),
            Arc(ojz, OJZ1),
            Arc(ojv, OJV1),
            Arc(ojs, OJS1),
            Arc(pj, OJZ1),
            Arc(pj, OJV1),
            Arc(pj, OJS1),
            Arc(OJV1, ov),
            Arc(OJZ1, oz),
            Arc(OJS1, os),

            Arc(rv, VZ),
            Arc(rv, VJ),
            Arc(rv, VS),
            Arc(VZ, vz),
            Arc(VJ, vj),
            Arc(VS, vs),
            Arc(vz, OVZ),
            Arc(vj, OVJ),
            Arc(vs, OVS),
            Arc(OVJ, ovj),
            Arc(OVZ, ovz),
            Arc(OVS, ovs),
            Arc(ovz, OVZ1),
            Arc(ovj, OVJ1),
            Arc(ovs, OVS1),
            Arc(pv, OVZ1),
            Arc(pv, OVJ1),
            Arc(pv, OVS1),
            Arc(OVJ1, oj),
            Arc(OVZ1, oz),
            Arc(OVS1, os),

            Arc(rz, ZJ),
            Arc(rz, ZV),
            Arc(rz, ZS),
            Arc(ZJ, zj),
            Arc(ZV, zv),
            Arc(ZS, zs),
            Arc(zv, OZV),
            Arc(zj, OZJ),
            Arc(zs, OZS),
            Arc(OZJ, ozj),
            Arc(OZV, ozv),
            Arc(OZS, ozs),
            Arc(ozv, OZV1),
            Arc(ozj, OZJ1),
            Arc(ozs, OZS1),
            Arc(pz, OZV1),
            Arc(pz, OZJ1),
            Arc(pz, OZS1),
            Arc(OZJ1, oj),
            Arc(OZV1, ov),
            Arc(OZS1, os),

            Arc(rs, SJ),
            Arc(rs, SV),
            Arc(rs, SZ),
            Arc(SJ, sj),
            Arc(SV, sv),
            Arc(SZ, sz),
            Arc(sv, OSV),
            Arc(sj, OSJ),
            Arc(sz, OSZ),
            Arc(OSJ, osj),
            Arc(OSV, osv),
            Arc(OSZ, osz),
            Arc(osv, OSV1),
            Arc(osj, OSJ1),
            Arc(osz, OSZ1),
            Arc(ps, OSV1),
            Arc(ps, OSJ1),
            Arc(ps, OSZ1),
            Arc(OSJ1, oj),
            Arc(OSV1, ov),
            Arc(OSZ1, oz),


            Inhibitor(cervena2, RJ),
            Inhibitor(pv, RJ),
            Inhibitor(pz, RJ),
            Inhibitor(ozj, OJZ1),
            Inhibitor(osz, OJZ1),

            Inhibitor(cervena1, RZ),
            Inhibitor(ps, RZ),
            Inhibitor(pj, RZ),
            Inhibitor(ovs, OZS1),
            Inhibitor(ovz, OZS1),


            Inhibitor(cervena2, RS),
            Inhibitor(pv, RS),
            Inhibitor(pz, RS),
            Inhibitor(ojs, OSV1),
            Inhibitor(ojv, OSV1),


            Inhibitor(cervena1, RV),
            Inhibitor(ps, RV),
            Inhibitor(pj, RV),
            Inhibitor(ozv, OVJ1),
            Inhibitor(ozj, OVJ1),

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

    petri_net_dump = dumps(petri_net.places, petri_net.transitions, petri_net.arcs)
    print(petri_net_dump)
    print('-----------------------------------------------')
    with open('krizovatky/X_krizovatka_semafor_2proud_ZV.json', 'w') as sem:
        sem.write(petri_net_dump)

    for t in places:
        print(t.name, t.tokens, sep=': ')

run()