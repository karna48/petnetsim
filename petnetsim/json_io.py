import json
import io
from itertools import starmap, chain
from .elements import *
from typing import List, Dict, Union


def load(file, context=default_context(), opts=None):
    if opts is None:
        opts = {}

    data = json.load(file)
    data['places'] = {int(k): v for k, v in data['places'].items()}
    data['transitions'] = {int(k): v for k, v in data['transitions'].items()}
    data['arcs'] = {int(k): v for k, v in data['arcs'].items()}
    names: List[str] = data['names']

    def make_place(name_idx: int, p: dict):
        name = names[name_idx]
        capacity = p.get('capacity', 'infinity')
        capacity = Place.INF_CAPACITY if capacity == 'infinity' else capacity
        return Place(name, p.get('init_tokens', 0), capacity, context=context)

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

            return TransitionTimed(name, t_min, t_max, dist_func, context=context)
        elif t_type == 'P':
            return TransitionPriority(name, t['p'], context=context)
        elif t_type == 'S':
            return TransitionStochastic(name, t['p'], context=context)
        elif t_type == 'N':
            return Transition(name, context=context)
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

        return cls(source, target, n_tokens, name, context=context)

    arcs = list(starmap(make_arc, data['arcs'].items()))

    return places, transitions, arcs


def dump(file, places, transitions, arcs, opts=None):
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
            raise RuntimeError('unknown arc type: ', str(type(t)))

    places_dump = {obj_idx_lookup[p]: dump_place(p) for p in places}
    transitions_dump = {obj_idx_lookup[t]: dump_transition(t) for t in transitions}
    arcs_dump = {obj_idx_lookup[a]: dump_arc(a) for a in arcs}

    json.dump({'names': names,
               'places': places_dump,
               'transitions': transitions_dump,
               'arcs': arcs_dump},
              file)


def loads(s, context=default_context(), opts=None):
    sio = io.StringIO(s)
    return load(sio, context, opts)


def dumps(places, transitions, arcs, opts=None):
    sio = io.StringIO()
    dump(sio, places, transitions, arcs, opts)
    return sio.getvalue()