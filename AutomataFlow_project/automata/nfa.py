"""Equivalent NFA obtained by eliminating epsilon transitions."""
from collections import defaultdict
from .regex_parser import EPSILON


class NFA:
    def __init__(self, states, alphabet, start, accepts, transitions):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.start = start
        self.accepts = set(accepts)
        self.transitions = defaultdict(set)
        for key, values in transitions.items():
            self.transitions[key] = set(values)

    @classmethod
    def from_enfa(cls, enfa):
        transitions = defaultdict(set)
        accepts = set()
        for state in enfa.states:
            closure = enfa.epsilon_closure({state})
            if enfa.accept in closure:
                accepts.add(state)
            for symbol in enfa.alphabet:
                destinations = enfa.move(closure, symbol)
                for dest in destinations:
                    transitions[(state, symbol)].update(enfa.epsilon_closure({dest}))
        return cls(enfa.states, enfa.alphabet, enfa.start, accepts, transitions)
