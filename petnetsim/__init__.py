import random
from .net import PetriNet


class Place:
    def __init__(self, name, capacity, init_tokens):
        self.name = name
        self.capacity = capacity
        self.init_tokens = init_tokens
        self.tokens = init_tokens

    def can_add(self, n_tokens):
        return self.tokens + n_tokens <= self.capacity

    def can_remove(self, n_tokens):
        return self.tokens - n_tokens >= 0

    def add(self, n_tokens):
        self.tokens += n_tokens

    def remove(self, n_tokens):
        self.tokens -= n_tokens

    def reset(self):
        pass


class Transition:
    def __init__(self, name):
        self.name = name


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
        return random.uniform(t_min, t_max)

    def reset(self):
        super().reset()
        self.timer.reset()


class Arc:
    def __init__(self, name, source, target, n_tokens):
        self.name = name
        self.source = source
        self.target = target
        self.n_tokens = n_tokens


class Inhibitor:
    def __init__(self, name, source, target, n_tokens):
        self.name = name
        self.source = source
        self.target = target
        self.n_tokens = n_tokens

