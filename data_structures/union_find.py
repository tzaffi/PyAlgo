from collections import defaultdict


class UnionFind:
    """
    Disjoint Set implementation
    """

    def __init__(self, universe):
        self._others = defaultdict(set)
        self._elts = set(universe)
        self._comp_count = len(self._elts)
        self._parent = {x: x for x in self._elts}

    ### Element Level Methods ###

    def union(self, x, y):
        parent_x, parent_y = self.find(x), self.find(y)
        if parent_x != parent_y:
            self._parent[parent_x] = parent_y

            self._comp_count -= 1

            self._others[parent_y] = self._others[parent_y].union(self._others[parent_x])
            self._others[parent_y].add(parent_x)
            del self._others[parent_x]

            return parent_y

    def find(self, x):
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def _get_rep_and_others(self, x):
        rep = self.find(x)
        return rep, self._others[rep]

    def component(self, x):
        rep, others = self._get_rep_and_others(x)
        return others.union({rep})

    def component_size(self, x):
        rep, others = self._get_rep_and_others(x)
        return 1 + len(others)

    def connected(self, x, y):
        return self.find(x) == self.find(y)

    ### Set Level Methods ###

    def __len__(self):
        return self._comp_count

    # def add(self, *elts):
    #     actually_added = False
    #     new_elts = set(elts)
    #     for x in new_elts:
    #         if x not in self._elts:
    #             actually_added = True
    #             self._elts.add(x)
    #             self._comp_count += 1
    #             self._parent[x] = x
    #     return actually_added

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if self._comp_count != other._comp_count:
            return False

        if self._elts != other._elts:
            return False

        for elt in self._elts:
            if self.component(elt) != other.component(elt):
                return False

        return True

    def __ne__(self, other):
        return not self == other
