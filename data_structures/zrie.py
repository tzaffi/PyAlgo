from __future__ import annotations
from typing import List, Optional, Dict, DefaultDict
from collections import defaultdict


class State:
    def __init__(self, prefix: str = "", accept: bool = False):
        """
        In the FSA case, `prefix` is just a label and can be ignored
        """
        self.prefix, self.accept = prefix, accept
        self.transitions: DefaultDict()[str, State] = defaultdict(list)
        self.radix_sort_keys: Optional[List[str]] = None

    def add_transition(self, c: str, target: State):
        assert len(c) == 1, f"transitions should be alphabetical, but given c={c}"
        self.transitions[c] = target

    def set_radix_sortable(self):
        self.radix_sort_keys = sorted(self.transitions.keys())

    def accepted(self, word: str):
        if not word:
            return self.accept
        c = word[0]
        return self.transitions[c].accepted(word[1:]) if c in self.transitions else False


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
        return self.start.accepted(word)


class DFA:
    pass
