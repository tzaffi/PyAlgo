from data_structures.zrie import Zrie, DFA
from itertools import product


def test_zrie_basic():
    words = ["cog", "dog", "dot", "hot", "log", "lot"]
    zrie = Zrie(words)
    assert sorted(words) == zrie.radix_sort()
    assert "cog" in zrie
    assert "cot" not in zrie
    for w in zrie:
        assert w in words

    words = ["apple", "cherry", "dragonfruit",  "banana"]
    zrie = Zrie(words)
    assert sorted(words) == list(zrie)

    words = {w[:i] for w in words for i in range(len(w)+1)}
    assert len(words) == 29
    zrie = Zrie(words)
    assert sorted(words) == list(zrie)


def test_dfa_basic():
    evens_init = {
        ("", False): [("0", "0")] + [(c, "odds") for c in "13579"] + [(c, "evens") for c in "2468"],
        ("0", True):  [],
        ("evens", True): [(c, "odds") for c in "13579"] + [(c, "evens") for c in "02468"],
        ("odds", False): [(c, "odds") for c in "13579"] + [(c, "evens") for c in "02468"],
    }
    evens = DFA("", evens_init)
    for i in range(100):
        if i % 2 == 0:
            assert str(i) in evens
        else:
            assert str(i) not in evens
    assert "" not in evens
    assert len(evens) == 4

    for i, e in enumerate(evens):
        print(e)
        # assert 2*i == int(e)
        if i > 10:
            break

    binary_evens_init = {
        ("0", True): [('0', "0"), ('1', "1")],
        ("1", False): [('0', "0"), ('1', "1")],
    }
    binary_evens = DFA("0", binary_evens_init)
    for x in map("".join, product(*([["0", "1"]]*5))):
        i = int(x, 2)
        if i % 2 == 0:
            assert x in binary_evens
        else:
            assert x not in binary_evens
    assert "" not in evens
    assert len(binary_evens) == 2

    assert evens.alphabet() == list(map(str, range(10)))
    assert binary_evens.alphabet() == ["0", "1"]


def test_dfa_minimization():
    words = ["cat", "dog", "eel", "fin", "gil", "hen"]
    zrie = Zrie(words)
    assert len(zrie) == 19
    assert list(zrie) == words
    mdfa = zrie.min_dfa()
    assert len(mdfa.alphabet()) == 12
    print(mdfa.states.keys())
    assert len(mdfa) == 12
    # assert list(mdfa) == list(zrie)
    assert "he" not in mdfa
    assert "hen" in mdfa
    assert list(mdfa) == list(zrie)
