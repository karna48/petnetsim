import io
import json
from itertools import starmap, chain
from typing import List, Union

from .elements import *


def load(file, context=default_context(), opts=None):
    if opts is None:
        opts = {}

    data = json.load(file)
    data['places'] = {int(k): v for k, v in data['places'].items()}
    data['transitions'] = {int(k): v for k, v in data['transitions'].items()}
    data['arcs'] = {int(k): v for k, v in data['arcs'].items()}
    graphics = data.get('graphics', None)
    names: List[str] = data['names']

    obj_lookup = {}

    if graphics is not None:
        graphics = {int(k): v for k, v in graphics.items()}

    def make_place(name_idx: int, p: dict):
        name = names[name_idx]
        capacity = p.get('capacity', 'infinity')
        capacity = Place.INF_CAPACITY if capacity == 'infinity' else capacity
        place = Place(name, p.get('init_tokens', 0), capacity, context=context)
        obj_lookup[name_idx] = place
        return place

    places = list(starmap(make_place, data['places'].items()))

    def make_transition(name_idx: int, t: dict):
        name = names[name_idx]
        t_type = t.get('T', 'N')
        if t_type == 'T':
            dist = t.get('dist', 'constant')
            if dist == 'constant':
                dist_func = constant_distribution
                t_min = t['t']
                t_max = 1  # unused value
            elif dist == 'uniform':
                dist_func = uniform_distribution
                t_min = t['t_min']
                t_max = t['t_max']
            elif dist == 'custom':
                dfs = opts.get('dist_functions', {})
                dfn = t['dist_func_name']
                dfuncs = [func for func, fname in dfs.items() if fname == dfn]
                t_min = t['t_min']
                t_max = t['t_max']
                if len(dfuncs) == 1:
                    dist_func = dfuncs[0]
                else:
                    raise RuntimeError('error in opts dist_functions for function: '+dfn)
            else:
                raise RuntimeError('unknown distribution: '+dist)
            transition = TransitionTimed(name, t_min, t_max, dist_func, context=context)
            obj_lookup[name_idx] = transition
            return transition
        elif t_type == 'P':
            transition = TransitionPriority(name, t['p'], context=context)
            obj_lookup[name_idx] = transition
            return transition
        elif t_type == 'S':
            transition = TransitionStochastic(name, t['p'], context=context)
            obj_lookup[name_idx] = transition
            return transition
        elif t_type == 'N':
            transition = Transition(name, context=context)
            obj_lookup[name_idx] = transition
            return transition
        else:
            raise RuntimeError('unknown transition type: '+str(t_type))

    transitions = list(starmap(make_transition, data['transitions'].items()))

    def make_arc(name_idx: int, arc: list):
        name = names[name_idx]
        offset = 0
        cls = Arc
        if isinstance(arc[0], str):
            if arc[0] == 'I':
                offset = 1
                cls = Inhibitor
            else:
                raise RuntimeError('unknown first string for arc:', arc[0])
        source = names[arc[offset]]
        target = names[arc[offset+1]]
        try:
            n_tokens = arc[offset+2]
        except IndexError:
            n_tokens = 1
        arc = cls(source, target, n_tokens, name, context=context)
        obj_lookup[name_idx] = arc
        return arc

    arcs = list(starmap(make_arc, data['arcs'].items()))

    if graphics is not None:
        graphics = {obj_lookup[name_idx]: g for name_idx, g in graphics.items()}

    return places, transitions, arcs, graphics


def dump(file, places, transitions, arcs, graphics, opts=None):
    opts = {} if opts is None else opts

    obj_idx_lookup = {x: i for i, x in enumerate(chain(places, transitions, arcs))}
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
                td.update({'dist': 'uniform', 't_min': t.t_min, 't_max': t.t_max})
            # TODO: add exponential and normal distributions at least
            else:
                if 'dist_functions' in opts:
                    dist_func_name = opts['dist_functions'].get(t.p_distribution_func, t.p_distribution_func.__name__)
                else:
                    dist_func_name = t.p_distribution_func.__name__
                td.update({'dist': 'custom',
                           'dist_func_name': dist_func_name,
                           't_min': t.t_min, 't_max': t.t_max})

            return td
        elif type(t) == TransitionPriority:
            return {'T': 'P', 'p': t.priority}
        elif type(t) == TransitionStochastic:
            return {'T': 'S', 'p': t.probability}
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
            raise RuntimeError('unknown arc type: ', str(type(a)))

    places_dump = {obj_idx_lookup[p]: dump_place(p) for p in places}
    transitions_dump = {obj_idx_lookup[t]: dump_transition(t) for t in transitions}
    arcs_dump = {obj_idx_lookup[a]: dump_arc(a) for a in arcs}

    data = {'names': names,
            'places': places_dump,
            'transitions': transitions_dump,
            'arcs': arcs_dump}

    if graphics is not None:
        data['graphics'] = {obj_idx_lookup[obj]: g for obj, g in graphics.items()}

    json.dump(data, file, indent=2)


def loads(s, context=default_context(), opts=None):
    sio = io.StringIO(s)
    return load(sio, context, opts)


def dumps(places, transitions, arcs, graphics=None, opts=None):
    sio = io.StringIO()
    dump(sio, places, transitions, arcs, graphics, opts)
    return sio.getvalue()
