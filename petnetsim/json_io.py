import json
import io
import itertools
from . import PetriNet, ConflictGroupType
from .elements import *
from typing import List, Dict, Union


def load(file, opts=None):
    if opts is None:
        opts = {}

    data = json.load(file)
    names: List[str] = data['names']

    def make_place(name_idx: str, p: dict):
        name = names[name_idx]
        capacity = p.get('capacity', 'infinity')
        capacity = Place.INF_CAPACITY if capacity == 'infinity' else capacity
        return Place(name, p.get('init_tokens', 0), capacity)

    places = [make_place(name_idx, p) for name_idx, p in data['places'].items()]

    def make_transition(name_idx: str, t: dict):
        name = names[name_idx]
        t_type = t.get('type', 'Normal')

    transitions = []

    arcs = []

    return places, transitions, arcs


def dump(file, places, transitions, arcs):
    obj_idx_lookup = {x: i for i, x in enumerate(itertools.chain(places, transitions, arcs))}
    names = [x.name for x in obj_idx_lookup.keys()]

    def dump_place(p: Place):
        pd = {}
        if p.init_tokens > 0:
            pd['init_tokens'] = p.init_tokens
        if p.capacity != Place.INF_CAPACITY:
            pd['capacity'] = p.capacity
        return pd

    def dump_transition(t: Union[Transition, TransitionTimed, TransitionStochastic, TransitionPriority]):
        # matching for exact type
        if type(t) == TransitionTimed:
            td = {'T': 'T'}
            if t.p_distribution_func == constant_distribution:
                td.update({'t': t.t_min})
            elif t.p_distribution_func == uniform_distribution:
                td = {'dist': 'uniform', 't_min': t.t_min, 't_max': t.t_max}
            else:
                td = {'dist': 'custom',
                      'dist_func_name': t.p_distribution_func.__name__,
                      't_min': t.t_min, 't_max': t.t_max}

            return td
        elif type(t) == TransitionPriority:
            return {'T': 'P', 'p': t.priority}
        elif type(t) == TransitionStochastic:
            return
        elif type(t) == Transition:
            return {}
        else:
            raise RuntimeError('unknown transition type: ', str(type(t)))

    def dump_arc(a: Union[Arc, Inhibitor]):
        v = [obj_idx_lookup[a.source], obj_idx_lookup[a.target]]
        if a.n_tokens > 1:
            v += [a.n_tokens]

        if type(a) == Arc:
            return v
        elif type(a) == Inhibitor:
            return ['I'] + v
        else:
            raise RuntimeError('unknown arc type: ', str(type(t)))

    places_dump = {obj_idx_lookup[p]: dump_place(p) for p in places}
    transitions_dump = {obj_idx_lookup[t]: dump_transition(t) for t in transitions}
    arcs_dump = {obj_idx_lookup[a]: dump_arc(a) for a in arcs}

    json.dump({'names': names,
               'places': places_dump,
               'transitions': transitions_dump,
               'arcs': arcs_dump})


def loads(s):
    sio = io.StringIO(s)
    return load(sio)


def dumps(places, transitions, arcs):
    sio = io.StringIO()
    dump(sio, places, transitions, arcs)
    return sio.getvalue()