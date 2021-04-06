from collections import defaultdict

from data_structures.union_find import UnionFind


class Graph:
    def __init__(self, adjacency_list=None):
        self.adjacency_list = defaultdict(list)

        if not adjacency_list:
            return

        for v1, edges in adjacency_list.items():
            self.add_vertex(v1)
            for v2 in edges:
                self.add_edge(v1, v2)

    def add_vertex(self, v):
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []

    def add_edge(self, v1, v2):
        self.adjacency_list[v1].append(v2)
        self.add_vertex(v2)

    def is_undirected(self):
        for v1, edges in self.adjacency_list.items():
            for v2 in edges:
                if v1 not in self.adjacency_list[v2]:
                    return False
        return True

    def get_components(self):
        assert self.is_undirected(), "Computing components requires an un-directed graph"

        vertices = self.adjacency_list.keys()

        comps = UnionFind(vertices)
        visited = set()

        def visit(v1):
            if v1 in visited:
                return
            visited.add(v1)

            for v2 in self.adjacency_list[v1]:
                comps.union(v1, v2)
                visit(v2)

        for v in vertices:
            visit(v)

        return comps.sets()
