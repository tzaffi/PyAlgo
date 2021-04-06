from data_structures.graph import Graph

from data_structures.tests.test_union_find import equal_sets_collection


def test_basic():
    adj_list = {
        1: [],
        2: [3, 4],
        3: [1, 3],
        4: [],
    }

    G = Graph()
    for v1, edges in adj_list.items():
        G.add_vertex(v1)
        for v2 in edges:
            G.add_edge(v1, v2)

    actual = G.adjacency_list
    assert actual == adj_list, actual


def test_is_undirected():
    directed_list = {
        1: [],
        2: [3, 4],
        3: [1, 3],
        4: [],
    }

    G = Graph(adjacency_list=directed_list)
    assert G.adjacency_list == directed_list
    assert not G.is_undirected()

    undirected_list = {
        1: [3],
        2: [3, 4],
        3: [1, 3, 2],
        4: [2],
    }

    G = Graph(adjacency_list=undirected_list)
    assert G.adjacency_list == undirected_list
    assert G.is_undirected()


def test_components():
    adj_list = {
        0: [5, 7],
        1: [3],
        2: [3, 4],
        3: [1, 3, 2],
        4: [2],
        5: [0],
        6: [],
        7: [0],
    }

    G = Graph(adjacency_list=adj_list)
    assert G.adjacency_list == adj_list
    assert G.is_undirected()

    expected = [{0, 5, 7}, {1, 2, 3, 4}, {6}]
    actual = G.get_components()
    assert equal_sets_collection(expected, actual), actual


test_components()
