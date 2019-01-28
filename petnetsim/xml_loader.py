from . import *
import xml.etree.ElementTree as ET
import math


def load_xml(filename):
    net = PetriNet()
    root = ET.parse(filename)

    for p_node in root.findall('place'):
        name = p_node.text

        capacity = p_node.attrib.get('capacity', math.inf)
        if capacity == 'inf':
            capacity = math.inf
        capacity = int(capacity) if isinstance(capacity, str) else capacity

        init_tokens = int(p_node.attrib.get('init_tokens', 0))

        p = Place(name, capacity, init_tokens)
        net.P.append(p)

    for t_node in root.findall('transition'):

        transition

    for a_node in root.findall('arc'):

    for i_node in root.findall('inhibitor'):

    net.validate(raise_=True)

    return net
