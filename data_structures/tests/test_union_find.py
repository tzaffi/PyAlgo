from data_structures.union_find import UnionFind


def test_init():
    ds = UnionFind([1, 2, 3])
    assert ds._elts == {1, 2, 3}
    assert ds._comp_count == 3
    assert ds._parent[2] == 2


def test_union_find():
    ds = UnionFind([1, 2, 3])
    assert ds.find(3) == 3

    assert 3 == ds.union(2, 3)
    assert ds.find(2) == ds.find(3)
    assert ds.find(1) != ds.find(3)


def test_component_n_size():
    ds = UnionFind([1, 2, 3])
    for i in [1, 2, 3]:
        assert ds.component(i) == {i}
        assert ds.component_size(i) == 1

    assert 3 == ds.union(2, 3)

    assert ds.component(1) == {1}
    assert ds.component(2) == {2, 3}

    assert ds.component_size(1) == 1
    assert ds.component_size(2) == 2


def test_connected():
    ds = UnionFind([1, 2, 3])
    for i in [1, 2, 3]:
        assert ds.connected(i, i)
        assert not ds.connected(i, i + 1 if i < 3 else 1)

    assert 3 == ds.union(2, 3)

    assert ds.connected(2, 3)
    assert not ds.connected(1, 3)


def test_eq_neq():
    ds1 = UnionFind([1, 2, 3])
    ds2 = UnionFind([1, 2, 3])

    assert ds1 == ds2
    assert not ds1 != ds2

    ds1.union(2, 3)
    assert not ds1 == ds2
    assert ds1 != ds2


def test_len():
    ds = UnionFind([1, 2, 3])
    assert len(ds) == 3

    ds.union(2, 3)
    assert len(ds) == 2

    ds.union(2, 3)
    assert len(ds) == 2

    ds.union(1, 2)
    assert len(ds) == 1
