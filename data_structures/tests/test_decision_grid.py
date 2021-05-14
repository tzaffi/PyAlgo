from itertools import product

from data_structures.decision_grid import DecisionGrid

dg_def = {
    2: 20,   # x < 2      ==> 20 <= y
    6: 10,   # 2 <= x < 6 ==> 10 <= y
    8:  5,   # 6 <= x < 8 ==>  5 <= y
             # 8 <= x     ==> APPROVE
}


def test_str():
    expected = "\n".join([
        'y',
        '20|********',
        '10|XX******',
        ' 5|XXXX****',
        ' 0|XXXXXX**',
        '--+0 2 6 8 x',
    ])
    actual = str(DecisionGrid(dg_def))
    print(expected)
    print(actual)
    assert len(expected) == len(actual)
    for i, e in enumerate(expected):
        a = actual[i]
        if e != a:
            print(i, e, ord(e), a, ord(a))
    assert expected == actual


def test_approved():
    decider = DecisionGrid(dg_def)
    for x, y in product(range(-1, 10), range(-1, 25)):
        if x < 2:
            expected_approved = y >= 20
        elif x < 6:
            expected_approved = y >= 10
        elif x < 8:
            expected_approved = y >= 5
        else:
            expected_approved = True
        actual = decider.is_approved(x, y)
        print(f"{(x,y)} -> {actual}")
        assert expected_approved == actual
