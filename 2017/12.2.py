import sys

import networkx as nx

def gen_edges(lines):
    for l in lines:
        left, rights = l.split(" <-> ")
        left_int = int(left)
        yield left_int, left_int
        right_ints = (int(r) for r in rights.split(", "))
        for r_int in right_ints:
            yield (left_int, r_int)

graph = nx.DiGraph()
graph.add_edges_from(gen_edges(sys.argv[1].splitlines()))
closure = nx.transitive_closure(graph)
cliques = list(nx.algorithms.clique.find_cliques_recursive(closure))
print(len(cliques))
