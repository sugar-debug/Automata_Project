"""DFA minimization using partition refinement."""
from collections import deque
from .dfa import DFA


def minimize_dfa(dfa):
    # First complete and remove states unreachable from the start.
    dfa = dfa.complete()
    reachable = {dfa.start}
    queue = deque([dfa.start])
    while queue:
        s = queue.popleft()
        for a in dfa.alphabet:
            t = dfa.transitions[(s, a)]
            if t not in reachable:
                reachable.add(t)
                queue.append(t)

    accepts = dfa.accepts & reachable
    nonaccepts = reachable - accepts
    partitions = [p for p in (accepts, nonaccepts) if p]

    changed = True
    while changed:
        changed = False
        new_partitions = []
        block_of = {s: i for i, block in enumerate(partitions) for s in block}
        for block in partitions:
            groups = {}
            for state in block:
                signature = tuple(block_of[dfa.transitions[(state, a)]] for a in sorted(dfa.alphabet))
                groups.setdefault(signature, set()).add(state)
            new_partitions.extend(groups.values())
            if len(groups) > 1:
                changed = True
        partitions = new_partitions

    # Give minimized states stable IDs by BFS from the start partition.
    block_of = {s: i for i, block in enumerate(partitions) for s in block}
    start_block = block_of[dfa.start]
    order = []
    seen = {start_block}
    queue = deque([start_block])
    while queue:
        bid = queue.popleft()
        order.append(bid)
        representative = next(iter(partitions[bid]))
        for a in sorted(dfa.alphabet):
            target_block = block_of[dfa.transitions[(representative, a)]]
            if target_block not in seen:
                seen.add(target_block)
                queue.append(target_block)

    new_id = {bid: i for i, bid in enumerate(order)}
    transitions = {}
    labels = {}
    new_accepts = set()
    for bid in order:
        sid = new_id[bid]
        block = partitions[bid]
        labels[sid] = "{" + ",".join(map(str, sorted(block))) + "}"
        if block & accepts:
            new_accepts.add(sid)
        representative = next(iter(block))
        for a in dfa.alphabet:
            target = block_of[dfa.transitions[(representative, a)]]
            transitions[(sid, a)] = new_id[target]

    return DFA(set(new_id.values()), dfa.alphabet, new_id[start_block], new_accepts, transitions, labels)
