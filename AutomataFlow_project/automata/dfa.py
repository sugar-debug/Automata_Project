"""Subset construction and deterministic string testing."""
from collections import deque, defaultdict
from .regex_parser import EPSILON


class DFA:
    def __init__(self, states, alphabet, start, accepts, transitions, labels=None):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.start = start
        self.accepts = set(accepts)
        self.transitions = dict(transitions)  # (state, symbol) -> state
        self.labels = labels or {s: str(s) for s in self.states}

    @classmethod
    def from_nfa(cls, nfa):
        start_set = frozenset({nfa.start})
        queue = deque([start_set])
        ids = {start_set: 0}
        transitions = {}
        accepts = set()
        labels = {0: "{" + ",".join(map(str, sorted(start_set))) + "}"}

        while queue:
            subset = queue.popleft()
            sid = ids[subset]
            if subset & nfa.accepts:
                accepts.add(sid)
            for symbol in sorted(nfa.alphabet):
                dest = set()
                for state in subset:
                    dest.update(nfa.transitions.get((state, symbol), set()))
                target = frozenset(dest)
                if target not in ids:
                    ids[target] = len(ids)
                    queue.append(target)
                    labels[ids[target]] = "{" + ",".join(map(str, sorted(target))) + "}"
                transitions[(sid, symbol)] = ids[target]
        return cls(set(ids.values()), nfa.alphabet, 0, accepts, transitions, labels)

    def run(self, string):
        current = self.start
        path = [current]
        for char in string:
            if char not in self.alphabet:
                return False, path, f"Symbol '{char}' is not in the automaton alphabet."
            key = (current, char)
            if key not in self.transitions:
                return False, path, "No transition for this symbol; string rejected."
            current = self.transitions[key]
            path.append(current)
        return current in self.accepts, path, ""

    def complete(self):
        """Return a completed DFA, adding a sink state for missing transitions."""
        transitions = dict(self.transitions)
        states = set(self.states)
        missing = [(s, a) for s in states for a in self.alphabet if (s, a) not in transitions]
        if not missing:
            return DFA(states, self.alphabet, self.start, self.accepts, transitions, dict(self.labels))
        sink = max(states, default=-1) + 1
        states.add(sink)
        labels = dict(self.labels)
        labels[sink] = "SINK"
        for s, a in missing:
            transitions[(s, a)] = sink
        for a in self.alphabet:
            transitions[(sink, a)] = sink
        return DFA(states, self.alphabet, self.start, self.accepts, transitions, labels)
