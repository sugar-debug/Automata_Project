import unittest
from automata.enfa import ENFA
from automata.nfa import NFA
from automata.dfa import DFA
from automata.minimizer import minimize_dfa


class AutomataTests(unittest.TestCase):
    def build(self, regex):
        return minimize_dfa(DFA.from_nfa(NFA.from_enfa(ENFA.from_regex(regex))))

    def test_regex_abb(self):
        dfa = self.build("(a|b)*abb")
        self.assertTrue(dfa.run("abb")[0])
        self.assertTrue(dfa.run("aabb")[0])
        self.assertFalse(dfa.run("abab")[0])
        self.assertFalse(dfa.run("ab")[0])

    def test_star(self):
        dfa = self.build("a*")
        self.assertTrue(dfa.run("")[0])
        self.assertTrue(dfa.run("aaa")[0])
        self.assertFalse(dfa.run("b")[0])

    def test_epsilon(self):
        dfa = self.build("ε")
        self.assertTrue(dfa.run("")[0])
        self.assertFalse(dfa.run("a")[0])


if __name__ == "__main__":
    unittest.main()
