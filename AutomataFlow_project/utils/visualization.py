"""Graphviz visualization and transition table helpers."""
from graphviz import Digraph


def automaton_graph(machine, title="Automaton", state_labels=None):
    graph = Digraph(name=title)
    graph.attr(rankdir="LR", label=title, labelloc="t")
    graph.attr("node", shape="circle")

    graph.node("__start", label="", shape="none")
    graph.edge("__start", str(machine.start))

    labels = state_labels or getattr(machine, "labels", {})

    accepting_states = (
        machine.accepts if hasattr(machine, "accepts")
        else {machine.accept}
    )

    for state in sorted(machine.states):
        label = labels.get(state, str(state))

        shape = (
            "doublecircle"
            if state in accepting_states
            else "circle"
        )

        graph.node(str(state), label=label, shape=shape)

    for key, targets in machine.transitions.items():
        source, symbol = key

        if isinstance(targets, (set, list, tuple)):
            for target in sorted(targets):
                graph.edge(str(source), str(target), label=symbol)
        else:
            graph.edge(str(source), str(targets), label=symbol)

    return graph

def transition_rows(machine):
    rows = []
    for state in sorted(machine.states):
        row = {"State": str(state)}
        for symbol in sorted(machine.alphabet):
            destinations = machine.transitions.get((state, symbol), set())
            if isinstance(destinations, set):
                row[symbol] = ",".join(map(str, sorted(destinations))) or "—"
            else:
                row[symbol] = str(destinations)
        rows.append(row)
    return rows
