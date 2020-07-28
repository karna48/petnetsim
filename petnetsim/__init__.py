from enum import IntEnum
import numpy as np
import random
from operator import attrgetter
from .elements import *
# from .xml_loader import load_xml


class ConflictGroupType(IntEnum):
    Normal = 0
    Priority = 1
    Stochastic = 2
    Timed = 3


class PetriNet:
    def __init__(self, places, transitions, arcs):
        self._names_lookup = {}
        for p in places:
            if p.name in self._names_lookup:
                raise RuntimeError('name reused: '+p.name)
            self._names_lookup[p.name] = p
        for t in transitions:
            if t.name in self._names_lookup:
                raise RuntimeError('name reused: '+t.name)
            self._names_lookup[t.name] = t

        for arc in arcs:
            if arc.name in self._names_lookup:
                raise RuntimeError('name reused: '+arc.name)
            self._names_lookup[arc.name] = arc
            arc.connect(self._names_lookup)

        for t in transitions:
            t.freeze()

        self.places = tuple(places)
        self.transitions = tuple(transitions)
        self.arcs = tuple(arcs)

        self._make_conflict_groups()

        self.enabled = np.zeros(len(transitions), dtype=np.bool)
        self._ended = False
        self.step_num = 0
        # fired in last step
        self.fired = []

    @property
    def ended(self):
        return self._ended

    def reset(self):
        self._ended = False
        self.step_num = 0
        self.fired.clear()
        for t in self.transitions:
            t.reset()
        for p in self.places:
            p.reset()

    def step(self, record_fired=True):
        if record_fired:
            self.fired.clear()
        # enabled transitions
        for ti, t in enumerate(self.transitions):
            self.enabled[ti] = t.enabled()

        CGT = ConflictGroupType

        enabled_any = self.enabled.any()
        if enabled_any:
            np.bitwise_and(self.enabled, self.conflict_groups_mask, out=self.enabled_conflict_groups)

            for cgi, ecg in enumerate(self.enabled_conflict_groups):
                if ecg.any():
                    cg_type = self.conflict_groups_types[cgi]
                    if cg_type == CGT.Normal:
                        t_idx = random.choice(np.argwhere(ecg))[0]


                    t_idx = random.choice(np.argwhere(ecg))[0]
                    t = self.transitions[t_idx]
                    t.fire()
                    if record_fired:
                        self.fired.append(t)

        num_waiting = 0
        if not enabled_any and num_waiting == 0:
            self._ended = True
        self.step_num += 1

    # def run(self, max_steps=None, max_sim_time=None):
    #     sim_time = 0.0

    def print_places(self):
        for p in self.places:
            print(p.name, p.tokens, sep=': ')

    def validate(self):
        # TODO : validation of whole net
        print('TODO: PetriNet.validate')
        pass

    def _make_conflict_groups(self):

        conflict_groups_sets = [{self.transitions[0]}]
        for t in self.transitions[1:]:
            add_to_cg = False
            # print('t: ', t.name)
            for cg in conflict_groups_sets:
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
                conflict_groups_sets.append([t])

        conflict_groups = tuple(tuple(sorted(cgs, key=attrgetter('name'))) for cgs in conflict_groups_sets)

        conflict_groups_types = [None for _ in conflict_groups_sets]

        def t_cg_type(transition):
            if isinstance(transition, TransitionPriority):
                return ConflictGroupType.Priority
            elif isinstance(transition, TransitionStochastic):
                return ConflictGroupType.Stochastic
            elif isinstance(transition, TransitionTimed):
                return ConflictGroupType.Timed
            return ConflictGroupType.Normal

        CGT = ConflictGroupType
        conflict_group_data = [None for _ in conflict_groups_sets]
        for cg_i, cg in enumerate(conflict_groups_sets):
            # cg type prefered by the transition
            t_types = [t_cg_type(t) for t in cg]

            if all(tt == CGT.Normal for tt in t_types):
                cg_type = CGT.Normal
            elif all(tt == CGT.Normal or tt == CGT.Priority for tt in t_types):
                # priority can be mixed with Normal
                cg_type = CGT.Priority
                conflict_group_data = np.zeros(len(self.transitions), dtype=np.bool)
            elif all(tt == CGT.Normal or tt == CGT.Timed for tt in t_types):
                # Timed can be mixed with Normal
                cg_type = CGT.Timed
            elif all(tt == CGT.Stochastic for tt in t_types):
                group_members_names = ', '.join([t.name for t in cg])
                # stochastic are on their own
                cg_type = CGT.Stochastic
                one_t_in_cg = next(iter(cg))
                if not all(t.inputs == one_t_in_cg.inputs for t in cg):
                    return RuntimeError('all members of stochastic group must share the same inputs: '+group_members_names)

                #if not all(t.inputs.n_tokens == one_t_in_cg.inputs.n_tokens for t in cg):
                #    RuntimeError('all members of stochastic group must take same number of tokens:'+group_members_names)

            else:
                raise RuntimeError('Unsupported combination of transitions: '+', '.join([str(tt) for tt in t_types]))

            conflict_groups_types[cg_i] = cg_type

        self.conflict_groups_sets = tuple(tuple(cg) for cg in conflict_groups_sets)
        self.conflict_groups_types = tuple(conflict_groups_types)
        self.conflict_groups_mask = np.zeros((len(conflict_groups_sets), len(self.transitions)), dtype=np.bool)
        self.enabled_conflict_groups = np.zeros((len(conflict_groups_sets), len(self.transitions)), dtype=np.bool)
        for cgi, (cg, cgt) in enumerate(zip(conflict_groups_sets, conflict_groups_types)):
            for ti, t in enumerate(self.transitions):
                t_in_cg = t in cg
                self.conflict_groups_mask[cgi, ti] = t_in_cg

                if t_in_cg:
                    if cgt == CGT.Priority:
                        conflict_group_data[cgi][ti] = t.priority if hasattr(t, 'priority') else 0
                    elif cgt == CGT.Timed:
                        conflict_group_data[cgi][ti] = isinstance(t, TransitionTimed)
                    elif cgt == CGT.Stochastic:
                        conflict_group_data[cgi][ti] = isinstance(t, TransitionTimed)

        self.conflict_group_data = tuple(conflict_group_data)