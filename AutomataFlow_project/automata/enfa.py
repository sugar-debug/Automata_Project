"""Thompson construction of an epsilon-NFA from postfix regular expressions."""
from collections import defaultdict
from .regex_parser import to_postfix, EPSILON, CONCAT


class ENFA:
    def __init__(self):
        self.transitions = defaultdict(set)  # (state, symbol) -> set(states)
        self.start = 0
        self.accept = 0
        self.states = set()
        self.alphabet = set()

    def add_transition(self, source, symbol, target):
        self.transitions[(source, symbol)].add(target)
        self.states.update((source, target))
        if symbol != EPSILON:
            self.alphabet.add(symbol)

    def move(self, states, symbol):
        result = set()
        for state in states:
            result.update(self.transitions.get((state, symbol), set()))
        return result

    def epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            for nxt in self.transitions.get((state, EPSILON), set()):
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
        return closure

    @classmethod
    def from_regex(cls, regex):
        postfix = to_postfix(regex)
        machine = cls()
        fragments = []
        next_state = 0

        def state():
            nonlocal next_state
            value = next_state
            next_state += 1
            machine.states.add(value)
            return value

        for token in postfix:
            if token not in {CONCAT, "|", "*", "+", "?"}:
                s, f = state(), state()
                machine.add_transition(s, EPSILON if token == EPSILON else token, f)
                fragments.append((s, f))
            elif token == CONCAT:
                if len(fragments) < 2:
                    raise ValueError("Invalid concatenation in regular expression.")
                s2, f2 = fragments.pop()
                s1, f1 = fragments.pop()
                machine.add_transition(f1, EPSILON, s2)
                fragments.append((s1, f2))
            elif token == "|":
                if len(fragments) < 2:
                    raise ValueError("Union operator '|' needs expressions on both sides.")
                s2, f2 = fragments.pop()
                s1, f1 = fragments.pop()
                start, final = state(), state()
                machine.add_transition(start, EPSILON, s1)
                machine.add_transition(start, EPSILON, s2)
                machine.add_transition(f1, EPSILON, final)
                machine.add_transition(f2, EPSILON, final)
                fragments.append((start, final))
            elif token == "*":
                if not fragments:
                    raise ValueError("Kleene star '*' needs an expression before it.")
                s, f = fragments.pop()
                start, final = state(), state()
                machine.add_transition(start, EPSILON, s)
                machine.add_transition(start, EPSILON, final)
                machine.add_transition(f, EPSILON, s)
                machine.add_transition(f, EPSILON, final)
                fragments.append((start, final))
            elif token == "+":
                if not fragments:
                    raise ValueError("Plus '+' needs an expression before it.")
                s, f = fragments.pop()
                start, final = state(), state()
                machine.add_transition(start, EPSILON, s)
                machine.add_transition(f, EPSILON, s)
                machine.add_transition(f, EPSILON, final)
                fragments.append((start, final))
            elif token == "?":
                if not fragments:
                    raise ValueError("Optional '?' needs an expression before it.")
                s, f = fragments.pop()
                start, final = state(), state()
                machine.add_transition(start, EPSILON, s)
                machine.add_transition(start, EPSILON, final)
                machine.add_transition(f, EPSILON, final)
                fragments.append((start, final))

        if len(fragments) != 1:
            raise ValueError("Invalid regular expression. Check operators and parentheses.")
        machine.start, machine.accept = fragments[0]
        return machine
