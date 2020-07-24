# from .net import PetriNet
from .elements import *
# from .xml_loader import load_xml

from enum import IntEnum


class ConflictGroupType(IntEnum):
    Normal = 0
    Priority = 1
    Stochastic = 2
    Timed = 3


def make_conflict_groups(transtions):

    conflict_groups = [{transitions[0]}]
    for t in transitions[1:]:
        add_to_cg = False
        # print('t: ', t.name)
        for cg in conflict_groups:
            for cg_t in cg:
                # ignore inhibitors!
                t_in = set(arc.source for arc in t.inputs if isinstance(arc, Arc))
                t_out = set(arc.target for arc in t.outputs if isinstance(arc, Arc))
                cg_t_in = set(arc.source for arc in cg_t.inputs if isinstance(arc, Arc))
                cg_t_out = set(arc.target for arc in cg_t.outputs if isinstance(arc, Arc))

                add_to_cg = add_to_cg or not t_in.isdisjoint(cg_t_in)
                add_to_cg = add_to_cg or not t_out.isdisjoint(cg_t_out)
                if add_to_cg:
                    break
            if add_to_cg:
                cg.add(t)
                break

        if not add_to_cg:
            conflict_groups.append([t])

    conflict_groups_types = []

    def t_cg_type(transition):
        if issubclass(transition, TransitionPriority):
            return ConflictGroupType.Priority
        elif issubclass(transition, TransitionStochastic):
            return ConflictGroupType.Stochastic
        elif issubclass(transition, TransitionTimed):
            return ConflictGroupType.Timed
        return ConflictGroupType.Normal

    CGT = ConflictGroupType

    for cg in conflict_groups:
        t_types = [t_cg_type(t) for t in cg]

        # any_normal = any(cg_type == CGT.Normal for t_type in t_types)
        # all_normal = any(cg_type == CGT.Normal for t_type in t_types)
        # any_priority_or_normal = any(cg_type == CGT.Normal for t_type in t_types)
        # all_normal = any(cg_type == CGT.Normal for t_type in t_types)

        if all(cg_type == CGT.Normal for t_type in t_types):
            cg_type = CGT.Normal
        elif:
            cg_type = CGT.Priority

        conflict_groups_types.append(cg_type)


    return conflict_groups, conflict_groups_types