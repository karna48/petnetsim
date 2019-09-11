from . import *
import xml.etree.ElementTree as ET
import math


def load_xml(filename):
    petri_net = PetriNet()
    root = ET.parse(filename)

    places_lookup = {}

    for place_node in root.findall('place'):
        name = place_node.text
        if name is None or len(name) == 0:
            raise ValueError('Transition must be named inside tag')

        capacity = place_node.attrib.get('capacity', math.inf)
        if capacity == 'inf':
            capacity = math.inf
        capacity = int(capacity) if isinstance(capacity, str) else capacity

        init_tokens = int(place_node.attrib.get('init_tokens', 0))

        p = Place(name, capacity, init_tokens)
        places_lookup[name] = p
        petri_net.P.append(p)

    transitions_lookup = {}

    for transition_node in root.findall('transition'):
        name = transition_node.text
        if name is None or len(name) == 0:
            raise ValueError('Transition must be named inside tag')

        transition_type = transition_node.attrib.get('type', 'normal')
        if transition_type == 'normal' or transition_type == 'priority':
            priority = transition_node.attrib.get('priority', None)
            if priority is None:
                t = Transition(name)
            else:
                t = TransitionPriority(name, int(priority))
        elif transition_type == 'timed':
            p_distribution = transition_node.attrib.get('p_distribution', 'constant')
            t_min = float(transition_node.attrib['t_min'])
            t_max = float(transition_node.attrib.get('t_max', t_min))
            if p_distribution == 'constant':
                p_distribution_func = TransitionTimed.constant_distribution
            elif p_distribution == 'uniform':
                p_distribution_func = TransitionTimed.uniform_distribution
            # TODO: exponential, normal
            else:
                raise AttributeError('unknown p_distribution for time: '+p_distribution)
            t = TransitionTimed(name, t_min, t_max, p_distribution_func)
        elif transition_type == 'stochastic':
            #TransitionStochastic
            pass

        transitions_lookup[name] = t
        petri_net.T.append(t)

    for arc_node in root.findall('arc'):
        name = arc_node.text
        source_name = arc_node.attrib['source']
        target_name = arc_node.attrib['target']
        n_tokens = arc_node.attrib.get('n_tokens', 1)
        if source_name in places_lookup and target_name in transitions_lookup:
            source = places_lookup[source_name]
            target = transitions_lookup[target_name]
        elif source_name in transitions_lookup and target_name in places_lookup:
            source = transitions_lookup[source_name]
            target = places_lookup[target_name]
        else:
            raise RuntimeError('Arc from "'+source_name+'" to "'+target_name+'" is not between place and transition')
        a = Arc(name, source, target, n_tokens)
        petri_net.A.append(a)

    for i_node in root.findall('inhibitor'):
        name = i_node.text
        source_name = i_node.attrib['source']
        target_name = i_node.attrib['target']
        n_tokens = i_node.attrib.get('n_tokens', 1)
        if source_name in places_lookup and target_name in transitions_lookup:
            source = places_lookup[source_name]
            target = transitions_lookup[target_name]
        else:
            raise RuntimeError('Inhibitor from "'+source_name+'" to "'+target_name+'" is not from place to transition')
        i = Inhibitor(name, source, target, n_tokens)
        petri_net.I.append(i)

    petri_net.validate()  # may raise exception

    return petri_net
