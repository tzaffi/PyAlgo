from __future__ import annotations
from typing import List, Optional, Dict, DefaultDict, Iterable
from collections import defaultdict, deque


class State:
    def __init__(self, prefix: str = "", accept: bool = False, verbose: bool = False):
        """
        In the FSA case, `prefix` is just a label and can be ignored
        """
        self.prefix, self.accept = prefix, accept
        self.transitions: DefaultDict()[str, State] = defaultdict(list)
        self.radix_sort_keys: Optional[List[str]] = None
        self.verbose = verbose

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
        return self.transitions[c].accepts(word[1:]) if c in self.transitions else False

    def __iter__(self) -> Iterable:
        yield self
        for k in self.radix_sort_keys:
            for s in self.transitions[k]:
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
                preorder(prefix + c, state.transitions[c])

        preorder("", self.start)
        return collected

    def __contains__(self, word: str) -> bool:
        return self.start.accepts(word)

    def __iter__(self) -> Iterable:
        def preorder(prefix, state):
            if state.accept:
                yield prefix
            for c in state.radix_sort_keys:
                yield from preorder(prefix+c, state.transitions[c])

        yield from preorder("", self.start)


class DFA:
    def __init__(self, start: str, transitions: Dict[Tuple[str, bool], List[Tuple[str, str]]]):
        self.states: Dict[str, State] = {}
        self.start: State = None

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
                q.append((prefix + c, state.transitions[c]))

    # def __iter__(self) -> Iterable:
    #     visited = set()

    #     def preorder(prefix, state):
    #         visited.add(prefix)
    #         print(visited)
    #         if state.accept:
    #             print(prefix)
    #             yield prefix
    #         for c in state.radix_sort_keys:
    #             if prefix+c not in visited:
    #                 yield from preorder(prefix + c, state.transitions[c])
    #     yield from preorder("", self.start)
