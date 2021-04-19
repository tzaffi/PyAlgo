from typing import Iterable


class Node:
    def __init__(self, x, left=None, right=None):  # , parent=None):
        self.x = x
        self.left, self.right = left, right
        # self.left, self.right, self.parent = left, right, parent
        self._reset_height()

    def imbalance(self):
        if not (self.left or self.right):
            return 0
        if not self.left:
            return -self.height
        if not self.right:
            return self.height
        return self.left.height - self.right.height

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        return self.x == other.x and self.height == other.height

    def __iter__(self):
        """
        Using the fact that `in` recursively calls `__iter__`
        """
        if self.left:
            for n in self.left:
                yield n

        yield self

        if self.right:
            for n in self.right:
                yield n

    def _reset_height(self):
        children = self.children()
        if not children:
            self.height = 0
            return

        self.height = 1 + max(map(lambda n: n.height, children))

    def is_leaf(self) -> bool:
        return not (self.left or self.right)

    def children(self) -> list:
        result = []
        if self.left:
            result.append(self.left)
        if self.right:
            result.append(self.right)
        return result

    def find(self, x):
        """
        Returns:
            None - if x not on my subtree
            node - if node holds x
        """
        if x == self.x:
            return self

        if x < self.x:
            return self.left.find(x) if self.left else None

        return self.right.find(x) if self.right else None

    def find_path(self, x) -> list:
        """
        path to node containing x - if it's in the tree
        else: None

        path is a list of type (Node, "left" or "right" or None)
        """
        if x == self.x:
            return [(self, None)]

        curr_res = rec_res = None
        if x < self.x:
            if not self.left:
                return None
            curr_res = [(self, "left")]
            rec_res = self.left.find_path(x)
        else:
            if not self.right:
                return None
            curr_res = [(self, "right")]
            rec_res = self.right.find_path(x)

        return curr_res + rec_res if rec_res else None


class Zree:
    """
    Elements should be comparable, but I'm not making it explicit.
    You could do this as described here: https://stackoverflow.com/questions/37669222/how-can-i-hint-that-a-type-is-comparable-with-typing
    """

    def __init__(self, verbose=False):
        self.root = None
        self.size = 0
        self.verbose = verbose

    def __len__(self):
        return self.size

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        def recurse_eq(snode, onode):
            if not snode:
                return not onode
            if not (snode == onode):
                return False
            return recurse_eq(snode.left, onode.left) and recurse_eq(snode.right, onode.right)

        return recurse_eq(self.root, other.root)

    def tree_str(self):
        res = []

        def dfs(node, child_type="", depth=0):
            res.append(" " * depth + child_type + f"{node.x}[ht={node.height}]")
            if node.left:
                dfs(node.left, child_type="L", depth=depth+1)
            if node.right:
                dfs(node.right, child_type="R", depth=depth+1)

        if self.root:
            dfs(self.root)

        else:
            res.append("Nothing to tree_print()!!!")

        return "\n".join(res)

    def height(self) -> int:
        if not self.root:
            return 0
        return self.root.height

    def add(self, x):
        self.size += 1
        self.root = self._add(x, self.root)

    def _add(self, x, node: Node) -> Node:
        """
        add a new node in order, __below__ the given node
        """
        if not node:
            return Node(x)

        if x < node.x:
            node.left = self._add(x, node.left)
            # node.left.parent = node
        else:
            node.right = self._add(x, node.right)
            # node.right.parent = node

        node._reset_height()
        return self._rebalance(node)

    def _rebalance(self, node: Node) -> Node:
        if abs(node.imbalance()) < 2:
            return node

        at_root = node == self.root
        # parent = node.parent

        if node.imbalance() < 0:
            if node.right.imbalance() > 0:
                node.right = self.rotate_right(node.right)
                # node.right.parent = node
            node = self.rotate_left(node)
            # node.parent = parent
            return node

        if node.left.imbalance() < 0:
            node.left = self.rotate_left(node.left)
            if self.verbose:
                print(self.tree_str())
            # node.left.parent = node
        node = self.rotate_right(node)
        if self.verbose:
            print(self.tree_str())
        # node.parent = parent
        if at_root:
            self.root = node
        return node

    def pluck_successor_as_root(self, node: Node) -> tuple:
        return self._pluck_as_root(node, successor=True)

    def pluck_predecessor_as_root(self, node: Node) -> tuple:
        return self._pluck_as_root(node, successor=False)

    def _pluck_as_root(self, node: Node, successor: bool = True) -> tuple:
        nxt = node.right if successor else node.left
        if not nxt:
            name = "successor" if successor else "predecessor"
            raise ValueError(f"there is no {name} to pluck")

        def nextor(n):
            return n.left if successor else n.right

        ancestors = []
        while nextor(nxt):
            ancestors.append(nxt)
            nxt = nextor(nxt)

        node.x = nxt.x
        if not ancestors:
            if successor:
                node.right = None
            else:
                node.left = None
        else:
            last_anc = ancestors[-1]
            if successor:
                last_anc.left = nxt.right
            else:
                last_anc.right = nxt.left
            desc = None
            for anc in ancestors[::-1]:
                if desc:
                    if successor:
                        anc.left = desc
                    else:
                        anc.right = desc
                anc._reset_height()
                desc = self._rebalance(anc)
            if successor:
                node.right = desc
            else:
                node.left = desc

        nxt_x = node.x
        node._reset_height()
        if self.verbose:
            print(f"BEFORE rebalance @{node.x}", "\n\n", f"{self.tree_str()}")
        node = self._rebalance(node)
        if self.verbose:
            print("AFTER rebalance:\n\n", f"{self.tree_str()}")

        return nxt_x, node

    def rotate_left(self, node: Node) -> Node:
        # parent = node.parent

        new_left, new_top, new_bottom = node, node.right, node.right.left
        new_left.right = new_bottom
        # new_left.right.parent = new_left

        new_top.left = new_left
        # new_top.left.parent = new_top

        new_left._reset_height()
        new_top._reset_height()

        if self.verbose:
            print(f"rotate_left'ed for {node.x}")

        return new_top

    def rotate_right(self, node: Node) -> Node:
        new_right, new_top, new_bottom = node, node.left, node.left.right
        new_right.left = new_bottom

        new_top.right = new_right

        new_right._reset_height()
        new_top._reset_height()

        if self.verbose:
            print(f"rotate_right'ed for {node.x}")

        return new_top

    def remove(self, x) -> None:
        # self.root = self._remove(x, self.root)

        if not self.root:
            raise ValueError(f"{x} not found")

        path = self.root.find_path(x)
        if not path:
            raise ValueError(f"{x} not found")

        node, direction = path.pop()
        assert node.x == x and direction is None

        if not path:
            assert node == self.root

        children = node.children()
        if len(children) == 2:
            if node.imbalance() > 0:
                node = self.pluck_predecessor_as_root(node)
            else:
                node = self.pluck_successor_as_root(node)
        else:
            node = node.left if node.left else node.right

        while path:
            parent, direction = path.pop()
            assert direction is not None
            if direction == "left":
                parent.left = node
            else:
                parent.right = node
            parent._reset_height()
            node = self._rebalance(parent)

        self.root = node
        self.size -= 1

    def __iter__(self):
        if self.root:
            for node in self.root:
                yield node.x

    def __contains__(self, x) -> bool:
        if not self.root:
            return False

        return self.root.find_path(x) is not None

    def minimum(self):
        if self.verbose:
            print("Zree custom minimum()")

        if not self.root:
            raise ValueError("minimum() arg is an empty sequence")

        node = self.root
        while node.left:
            node = node.left

        return node.x

    def maximum(self):
        if self.verbose:
            print("Zree custom maximum()")

        if not self.root:
            raise ValueError("maximum() arg is an empty sequence")

        node = self.root
        while node.right:
            node = node.right

        return node.x


class SortedList:
    """
    My own AVL-tree based Sorted List.
    Inspired by: https://stackoverflow.com/questions/37669222/how-can-i-hint-that-a-type-is-comparable-with-typing

    Example:
    >>> sl = SortedList(range(1000))            # construct using an iterable of a comparable in O(N * log N)
    >>> sl.add(-4).add(-5).add(42).add(1337)    # add some more comparables each time in O(log N)
    >>> assert len(sl) == 1004                  # you can get its length in O(1)
    >>> assert 42 in sl                         # you can check for containment in O(log N)
    >>> for x in sl: print(x)                   # you can iterate through the entire list in O(N)
    >>> assert sl != SortedList(range(1004))    # you can test for equality in O(N)
    >>> sl.tree_print()                         # you can print a pre-order traversal in O(N)
    >>> assert sl.minimum() == -5               # you can get the min in O(log N) (but the built-in will be slower)
    >>> assert sl.maximum() == 1337             # you can get the max in O(log N) (but the built-in will be slower)
    >>> sl.remove(1337)                         # you can remove an element in O(log N)
    """

    def __init__(self, it: Iterable = [], verbose: bool = False):
        self._zree = Zree(verbose=verbose)
        for x in it:
            self.add(x)

    def add(self, x):
        self._zree.add(x)
        return self

    def remove(self, x):
        """
        Raises a ValueError if `x not in self`
        """
        self._zree.remove(x)

    def tree_print(self):
        print(self._zree.tree_str())

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        DNE = "SENTINEL FOR HAS NO NEXT"
        other_iter = iter(other)
        for x in self:
            y_or_DNE = next(other_iter, DNE)
            if x != y_or_DNE:
                return False
        if next(other_iter, DNE) != DNE:
            return False

        return True

    def __iter__(self):
        for x in self._zree:
            yield x

    def __contains__(self, x) -> bool:
        return x in self._zree

    def __len__(self):
        return 0 if not self._zree else len(self._zree)

    def minimum(self):
        return self._zree.minimum()

    def maximum(self):
        return self._zree.maximum()
