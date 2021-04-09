from contextlib import redirect_stdout
import io

from data_structures.avl_tree import AVLTree


def test_basic():
    bst = AVLTree()
    bst.insert(1)
    bst.insert(2)
    bst.insert(3)
    bst.insert(4)
    bst.insert(5)
    bst.insert(6)
    bst.insert(7)
    bst.insert(8)

    f = io.StringIO()
    with redirect_stdout(f):
        bst.prettyPrint()

    assert f.getvalue() == """R----4
     L----2
     |    L----1
     |    R----3
     R----6
          L----5
          R----7
               R----8
"""
