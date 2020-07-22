import random as _random
import math


class Place:
    INF_CAPACITY = 0
    _annonymous_counter = 1

    def __init__(self, name=None, init_tokens=0, capacity=INF_CAPACITY):
        if name is None:
            self.name = 'P_'+str(Place._annonymous_counter)
            Place._annonymous_counter += 1
        else:
            self.name = name
        self.capacity = capacity
        self.init_tokens = init_tokens
        self.tokens = init_tokens

    def can_add(self, n_tokens):
        return self.capacity == Place.INF_CAPACITY or self.tokens + n_tokens <= self.capacity

    def can_remove(self, n_tokens):
        return self.tokens - n_tokens >= 0

    def add(self, n_tokens):
        self.tokens += n_tokens

    def remove(self, n_tokens):
        self.tokens -= n_tokens

    def reset(self):
        self.tokens = self.init_tokens


class Transition:
    _annonymous_counter = 1

    def __init__(self, name):
        if name is None:
            self.name = 'T_'+str(Transition._annonymous_counter)
            Transition._annonymous_counter += 1
        else:
            self.name = name
        self.inputs = set()   # Arc
        self.outputs = set()  # Arc
        self.fired_times = 0

    def enabled(self):
        return all(arc.source.can_remove(arc.n_tokens) for arc in self.inputs) \
               and all(arc.target.can_add(arc.n_tokens) for arc in self.outputs)

    def fire(self):
        for arc in self.inputs:
            arc.source.remove(arc.n_tokens)

        for arc in self.outputs:
            arc.target.add(arc.n_tokens)

        self.fired_times += 1

    def reset(self):
        self.fired_times = 0


class TransitionPriority(Transition):
    def __init__(self, name, priority):
        super().__init__(name)
        self.priority = priority

    def reset(self):
        super().reset()


class TransitionTimed(Transition):
    T_EPSILON = 1e6

    def __init__(self, name, t_min, t_max, p_distribution_func):
        super().__init__(name)
        self.remaining = 0
        self.t_min = t_min
        self.t_max = t_max
        self.p_distribution_func = p_distribution_func

    @staticmethod
    def constant_distribution(t_min, t_max):
        return t_min

    @staticmethod
    def uniform_distribution(t_min, t_max):
        return _random.uniform(t_min, t_max)

    def enabled(self):
        return super().enabled() and self.remaining <= 0

    def enabled_waiting(self):
        return super().enabled() and self.remaining > 0

    def reset_remaining(self):
        self.remaining = self.p_distribution_func(self.t_min, self.t_max)

    def fire(self):
        super().fire()
        self.reset_remaining()

    def reset(self):
        super().reset()
        self.reset_remaining()


class TransitionStochastic(Transition):
    def __init__(self, name, probability):
        super().__init__(name)
        self.probability = probability

    def reset(self):
        super().reset()


class Arc:
    _annonymous_counter = 1

    def __init__(self, source, target, n_tokens, name=None):
        if name is None:
            self.name = 'Arc_'+str(Arc._annonymous_counter)
            Arc._annonymous_counter += 1
        else:
            self.name = name
        self.name = name
        self.source = source
        self.target = target
        self.n_tokens = n_tokens
        if isinstance(source, Transition):
            source.outputs.add(self)
        if isinstance(target, Transition):
            target.inputs.add(self)


class Inhibitor:
    _annonymous_counter = 1

    def __init__(self, name, source, target, n_tokens):
        if name is None:
            self.name = 'Arc_'+str(Inhibitor._annonymous_counter)
            Inhibitor._annonymous_counter += 1
        else:
            self.name = name
        self.source = source
        self.target = target
        self.n_tokens = n_tokens
