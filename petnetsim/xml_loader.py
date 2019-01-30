from . import *
import xml.etree.ElementTree as ET
import math


def load_xml(filename):
    petri_net = PetriNet()
    root = ET.parse(filename)

    P_d = {}

    for p_node in root.findall('place'):
        name = p_node.text
        if name is None or len(name)==0:
            raise ValueError('Transition must be named inside tag')

        capacity = p_node.attrib.get('capacity', math.inf)
        if capacity == 'inf':
            capacity = math.inf
        capacity = int(capacity) if isinstance(capacity, str) else capacity

        init_tokens = int(p_node.attrib.get('init_tokens', 0))

        p = Place(name, capacity, init_tokens)
        P_d[name] = p
        petri_net.P.append(p)

    T_d = {}

    for t_node in root.findall('transition'):
        name = t_node.text
        if name is None or len(name)==0:
            raise ValueError('Transition must be named inside tag')

        t_type = t_node.attrib.get('type', 'normal')
        if t_type == 'normal' or t_type == 'priority':
            priority = t_node.attrib.get('priority', None)
            if priority is None:
                t = Transition(name)
            else:
                t = TransitionPriority(name, int(priority))
        elif t_type == 'timed':
            p_distribution = t_node.attrib.get('p_distribution', 'constant')
            t_min = float(t_node.attrib['t_min'])
            t_max = float(t_node.attrib.get('t_max', t_min))
            if p_distribution == 'constant':
                p_distribution_func = TransitionTimed.constant_distribution
            elif p_distribution == 'uniform':
                p_distribution_func = TransitionTimed.uniform_distribution
            # TODO: exponential, normal
            else:
                raise AttributeError('unknown p_distribution for time: '+p_distribution)
            t = TransitionTimed(name, t_min, t_max, p_distribution_func)
        elif t_type == 'stochastic':
            #TransitionStochastic
            pass

        T_d[name] = t
        petri_net.T.append(t)

    for a_node in root.findall('arc'):
        name = a_node.text
        source_name = a_node.attrib['source']
        target_name = a_node.attrib['target']
        n_tokens = a_node.attrib.get('n_tokens', 1)
        if source_name in P_d and target_name in T_d:
            source = P_d[source_name]
            target = T_d[target_name]
        elif source_name in T_d and target_name in P_d:
            source = P_d[source_name]
            target = T_d[target_name]
        else:
            raise RuntimeError('Arc from "'+source_name+'" to "'+target_name+'" is not between place and transition')
        a = Arc(name, source, target, n_tokens)
        petri_net.A.append(a)

    for i_node in root.findall('inhibitor'):
        name = i_node.text
        source_name = i_node.attrib['source']
        target_name = i_node.attrib['target']
        n_tokens = i_node.attrib.get('n_tokens', 1)
        if source_name in P_d and target_name in T_d:
            source = P_d[source_name]
            target = T_d[target_name]
        else:
            raise RuntimeError('Inhibitor from "'+source_name+'" to "'+target_name+'" is not from place to transition')
        i = Inhibitor(name, source, target, n_tokens)
        petri_net.I.append(i)

    petri_net.validate()  # may raise exception

    return petri_net
