from __future__ import annotations
from typing import List, Optional, Dict, DefaultDict, Iterable, Set
from collections import defaultdict, deque
from functools import reduce


class State:
    def __init__(self, prefix: str = "", accept: bool = False, verbose: bool = False):
        """
        In the FSA case, `prefix` is just a label and can be ignored
        """
        self.prefix, self.accept = prefix, accept
        self.transitions: DefaultDict()[str, State] = defaultdict(list)
        self.radix_sort_keys: Optional[List[str]] = None
        self.verbose = verbose

    def __call__(self, c: str) -> State:
        return self.transitions[c]

    def __eq__(self, other: State) -> bool:
        if not isinstance(other, State):
            return False
        return self.prefix == other.prefix

    def __hash__(self) -> int:
        return hash(self.prefix)

    def __str__(self) -> str:
        return f"({self.prefix})"

    def __repr__(self) -> str:
        return str(self)

    def add_transition(self, c: str, target: State):
        assert len(c) == 1, f"transitions should be alphabetical, but given c={c}"
        self.transitions[c] = target

    def set_radix_sortable(self):
        self.radix_sort_keys = sorted(self.transitions.keys())

    def accepts(self, word: str):
        if self.verbose:
            print(f"{self.prefix}[{'accept' if self.accept else 'reject'}].accepts({word})?")
        if not word:
            return self.accept
        c = word[0]
        return self(c).accepts(word[1:]) if c in self.transitions else False

    def __iter__(self) -> Iterable:
        yield self
        for k in self.radix_sort_keys:
            for s in self(k):
                yield s


class Zrie:
    """
    Classical Prefix Trie that is Radix-Sortable
    """

    def __init__(self, words: List[str]):
        self.words = set(words)
        self.max_len = max(len(w) for w in words)
        self.states: Dict[str, State] = {}

        self.start = State(accept=("" in self.words))
        self.states[""] = self.start

        for w in self.words:
            for i in range(len(w), -1, -1):
                prefix = w[:i]
                is_entire_word = (i == len(w))
                if prefix not in self.states:
                    self.states[prefix] = State(prefix=prefix)
                state = self.states[prefix]
                if is_entire_word:
                    state.accept = True
                else:
                    state.add_transition(w[i], self.states[w[:i+1]])

        for state in self.states.values():
            state.set_radix_sortable()

    def radix_sort(self) -> List[str]:
        collected = []

        def preorder(prefix, state):
            if state.accept:
                collected.append(prefix)
            for c in state.radix_sort_keys:
                preorder(prefix + c, state(c))

        preorder("", self.start)
        return collected

    def __contains__(self, word: str) -> bool:
        return self.start.accepts(word)

    def __iter__(self) -> Iterable:
        def preorder(prefix, state):
            if state.accept:
                yield prefix
            for c in state.radix_sort_keys:
                yield from preorder(prefix+c, state(c))

        yield from preorder("", self.start)

    def __len__(self) -> int:
        return len(self.states)

    def min_dfa(self) -> DFA:
        dfa = DFA("", {}, for_clone=True)
        dfa.states = self.states
        dfa.start = self.start
        return dfa.minimize()


class DFA:
    def __init__(
        self,
        start: str,
        transitions: Dict[Tuple[str, bool],
                          List[Tuple[str, str]]],
        for_clone=False
    ):
        self.states: Dict[str, State] = {}
        self.start: State = None
        if for_clone:
            return

        for state_accept, translist in transitions.items():
            state, accept = state_accept
            if state not in self.states:
                self.states[state] = State(prefix=state)
            s = self.states[state]
            s.accept = accept

            if state == start:
                self.start = s

            for c, target in translist:
                assert isinstance(c, str)
                assert len(c) == 1
                if target not in self.states:
                    self.states[target] = State(prefix=target)
                s.transitions[c] = self.states[target]

        assert self.start is not None
        for state in self.states.values():
            state.set_radix_sortable()

    def __len__(self) -> int:
        return len(self.states)

    def __contains__(self, word: str) -> bool:
        return self.start.accepts(word)

    def __iter__(self) -> Iterable:
        """
        Iterate by order of length and lexicographically
        """
        q = deque([("", self.start)])
        while q:
            prefix, state = q.popleft()
            if state.accept:
                yield prefix
            for c in state.radix_sort_keys:
                q.append((prefix + c, state(c)))

    def alphabet(self):
        return sorted({c for s in self.states.values() for c in s.transitions.keys()})

    def minimize(self) -> DFA:
        TERMINUS = "><"
        assert TERMINUS not in self.states.keys()
        dead = State(prefix=TERMINUS)

        def label(ss):
            return "|".join(sorted(map(lambda s: s.prefix, ss)))

        class StatePartition:
            def __init__(self, ss: List[Set[State]]):
                # print(ss)
                self.partition = {}
                self.reverse_idx = {}
                self.terminus = None
                for states in ss:
                    lbl = label(states)
                    st_set = set(states)
                    self.partition[lbl] = st_set
                    for s in st_set:
                        self.reverse_idx[s] = lbl
                        if s.prefix == TERMINUS:
                            self.terminus = s
                assert self.terminus, "must have a terminus"
                # print(self.partition.keys())

            def __len__(self) -> int:
                return len(self.partition)

            def split(self, c) -> StatePartition:
                splits = {}
                for states in self.partition.values():
                    targets = defaultdict(set)
                    for s in states:
                        target = self.terminus if c not in s.transitions else s(c)
                        targets[self.reverse_idx[target]].add(s)
                    if len(targets) > 1:
                        splits[self.reverse_idx[s]] = targets.values()

                if not splits:
                    # print(f"No split for {c}")
                    return self

                # print(splits)
                # print("1.", [list(v) for v in splits.values()])
                # print("2.", reduce(lambda x, y: x+y,  [list(v) for v in splits.values()]))
                # new_partition = [list(states)[0] for states in splits.values()]
                new_partition = reduce(lambda x, y: x+y,  [list(v) for v in splits.values()])
                # print("just the new", new_partition)
                for lbl, states in self.partition.items():
                    if lbl not in splits:
                        new_partition.append(states)
                # print("plus the old", new_partition)
                return StatePartition(new_partition)

        alph = self.alphabet()

        a_states, f_states = set(), {dead}
        for s in self.states.values():
            (a_states if s.accept else f_states).add(s)

        partition = StatePartition([a_states, f_states])
        grew_states = True
        while grew_states:
            grew_states = False
            for c in alph:
                new_partition = partition.split(c)
                if len(new_partition) > len(partition):
                    partition = new_partition
                    grew_states = True
                    continue

        start = None
        transitions = defaultdict(list)  # Dict[Tuple[str, bool], List[Tuple[str, str]]]
        for part in partition.partition.values():
            for state in part:
                lbl = partition.reverse_idx[state]
                if state == self.start:
                    start = lbl
            for state in part:
                for c in alph:
                    tgt = state(c) if c in state.transitions else dead
                    tgt_lbl = partition.reverse_idx[tgt]
                    transitions[(lbl, state.accept)].append((c, tgt_lbl))
                break

        print(transitions.keys())
        # remove the terminal state -if we can- for finiteness
        term_lbl = partition.reverse_idx[dead]
        is_terminal = False
        if (term_lbl, False) in transitions:
            # print("HIYA")
            if {tgt for _, tgt in transitions[(term_lbl, False)]} == {term_lbl}:
                is_terminal = True
        if is_terminal:
            del transitions[(term_lbl, False)]
            print("DELETING")
            transitions = {k: [w for w in v if w[1] != term_lbl] for k, v in transitions.items()}
        # print(transitions)

        return DFA(start, transitions)
