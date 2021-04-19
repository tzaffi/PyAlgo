from data_structures.zrie import Zrie, DFA


def test_zrie_basic():
    words = ["cog", "dog", "dot", "hot", "log", "lot"]
    zrie = Zrie(words)
    assert sorted(words) == zrie.radix_sort()
    assert "cog" in zrie
    assert "cot" not in zrie


# def test_dfa_basic():
#     words = ["cog", "dog", "dot", "hot", "log", "lot"]
#     dfa = DFA(words)
#     mdfa = dfa.minimize()
