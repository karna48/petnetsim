from . import *
import xml.etree.ElementTree as ET
import math


def load_xml(filename):
    net = PetriNet()
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
        net.P.append(p)

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
        # TODO
        # elif t_type == 'timed':
        #     priority = t_node.attrib.get('priority', None)
        # elif t_type == 'stochastic':


        T_d[name] = t
        net.T.append(t)

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
            raise RuntimeError('Arc between "'+source_name+'" and "'+target_name+'" is not between place and transitions')
        a = Arc(name, source, target, n_tokens)
        net.A.append(a)

    for i_node in root.findall('inhibitor'):
        if source_name in P_d and target_name in T_d:
        i = Inhibitor()

    net.validate()  # may raise exception

    return net
