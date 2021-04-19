import math
import random

import pytest


from data_structures.zree import SortedList


def test_pluck_successor_as_root():
    verbose = False

    small = SortedList().add(5).add(0).add(10).add(3).add(7)

    print("small.tree_print()")
    small.tree_print()

    assert small == small

    pluck = small._zree
    assert pluck == pluck

    pluck.pluck_successor_as_root(pluck.root)

    small2 = SortedList(verbose=verbose).add(7).add(0).add(10).add(3)

    print("small2.tree_print()")
    small2.tree_print()

    assert small2._zree == pluck

    small2._zree.pluck_successor_as_root(small2._zree.root)
    print("small2.tree_print() AGAIN")
    small2.tree_print()

    small2._zree.root = small2._zree._rebalance(small2._zree.root)
    print("small2.tree_print() AND AGAIN")
    small2.tree_print()

    small3 = SortedList([3, 0, 10])
    print("small3.tree_print()")
    small3.tree_print()

    assert small3 == small2

    small2._zree.pluck_successor_as_root(small2._zree.root)
    print("small2.tree_print() SHOULD HAVE 10 ON TOP WITH NO SUCCESSOR")
    small2.tree_print()

    with pytest.raises(ValueError) as ve:
        small2._zree.pluck_successor_as_root(small2._zree.root)
    assert "no successor to pluck" in str(ve.value)
    print("small2.tree_print() SHOULD __still__ HAVE 10 ON TOP WITH NO SUCCESSOR")
    small2.tree_print()

    bigger = SortedList(range(100))
    if verbose:
        print("bigger.tree_print()")
        bigger.tree_print()

    bigger2 = SortedList(range(63))
    for i in range(64, 100):
        bigger2.add(i)
    if verbose:
        print("bigger2.tree_print()")
        bigger2.tree_print()

    bigger._zree.pluck_successor_as_root(bigger._zree.root)

    if verbose:
        print("bigger.tree_print() AGAIN")
        bigger.tree_print()

    bigger._zree.root = bigger._zree._rebalance(bigger._zree.root)
    if verbose:
        print("bigger.tree_print() AND AGAIN")
        bigger.tree_print()

    assert bigger._zree.root == bigger2._zree.root


def test_pluck_predecessor_as_root():
    verbose = True

    small = SortedList().add(5).add(0).add(10).add(3).add(7)

    print("small.tree_print()")
    small.tree_print()

    assert small == small

    pluck = small._zree
    assert pluck == pluck

    pluck.pluck_predecessor_as_root(pluck.root)

    small2 = SortedList(verbose=verbose).add(3).add(0).add(10).add(7)

    print("small2.tree_print()")
    small2.tree_print()

    assert small2._zree == pluck

    _, small2._zree.root = small2._zree.pluck_predecessor_as_root(small2._zree.root)
    print("small2.tree_print() AGAIN")
    small2.tree_print()

    small2._zree.root = small2._zree._rebalance(small2._zree.root)
    print("small2.tree_print() AND AGAIN")
    small2.tree_print()

    small3 = SortedList([7, 0, 10])
    print("small3.tree_print()")
    small3.tree_print()

    assert small3 == small2

    small2._zree.pluck_predecessor_as_root(small2._zree.root)
    print("small2.tree_print() SHOULD HAVE 0 ON TOP WITH NO PREDECESSOR")
    small2.tree_print()

    with pytest.raises(ValueError) as ve:
        small2._zree.pluck_predecessor_as_root(small2._zree.root)
    assert "no predecessor to pluck" in str(ve.value)
    print("small2.tree_print() SHOULD __still__ HAVE 0 ON TOP WITH NO PREDECESSOR")
    small2.tree_print()

    bigger = SortedList(range(100))
    if verbose:
        print("bigger.tree_print()")
        bigger.tree_print()

    assert len(bigger) == 100
    root = bigger._zree.root
    prev_root_val = root.x
    for i in range(100):
        try:
            expected_pred = max(j for j in bigger if j < prev_root_val)
        except ValueError as ve:
            assert i == 97
            assert "max() arg is an empty sequence" == str(ve)
            break

        before_fail = bigger._zree.tree_str()
        _, root = pred_x, bigger._zree.root = bigger._zree.pluck_predecessor_as_root(bigger._zree.root)
        print(f"{i}'th iteration {prev_root_val} -> ({pred_x}, {root.x})")

        if pred_x != expected_pred:
            print(before_fail)
        assert pred_x == expected_pred
        prev_root_val = root.x

    with pytest.raises(ValueError) as ve:
        bigger._zree.pluck_predecessor_as_root(bigger._zree.root)
    assert "no predecessor to pluck" in str(ve.value)


def test_list():
    assert list(SortedList(list("leet"))) == ["e", "e", "l", "t"]


def test_big():
    verbose = False
    random.seed(42)

    # first check the random seed is working
    five = [random.randrange(42) for _ in range(5)]
    assert five == [40, 7, 1, 17, 15]

    thousand = [random.randrange(100000) for _ in range(1000)]

    thou_zsl = SortedList(thousand)
    assert list(thou_zsl) == sorted(thousand)

    length = len(thou_zsl)
    assert length == 1000

    height = thou_zsl._zree.height()
    assert height == 11
    assert height < 1.45 * math.log(length, 2)

    thou_srtd = SortedList(range(1000), verbose=verbose)
    assert list(thou_srtd) == list(range(1000))

    length = len(thou_srtd)
    assert length == 1000

    height = thou_srtd._zree.height()
    assert height == 9
    assert height < 1.45 * math.log(length, 2)

    thou_srtd2 = SortedList()
    for i in range(1000):
        thou_srtd2.add(i)

    assert len(thou_srtd2) == 1000
    assert thou_srtd2 == thou_srtd
    # assert thou_srtd2.__eq__(thou_srtd)

    for i in range(1000):
        assert thou_srtd
        length = len(thou_srtd)
        assert length == 1000 - i
        assert thou_srtd._zree.height() <= 1.45 * math.log(length, 2)
        assert i - 1 not in thou_srtd
        assert i in thou_srtd
        assert i == min(thou_srtd)
        thou_srtd.remove(i)

    assert not thou_srtd
    assert len(thou_srtd) == 0
    assert thou_srtd._zree.height() == 0
    assert -1 not in thou_srtd


def test_equals():
    sl1 = SortedList(range(1000))
    sl2 = SortedList(range(999, -1, -1))
    sl3 = SortedList(range(1000))

    assert sl1 == sl2
    assert sl1._zree != sl2._zree

    assert sl1 == sl3
    assert sl1._zree == sl3._zree


def test_class_comment():
    verbose = False

    sl = SortedList(range(1000), verbose=verbose)
    sl.add(-4).add(-5).add(42).add(1337)
    assert len(sl) == 1004
    assert 42 in sl
    for _ in sl:
        pass
    assert sl != SortedList(range(1004))
    if verbose:
        sl.tree_print()
    assert sl.minimum() == -5
    assert sl.maximum() == 1337
    sl.remove(1337)
