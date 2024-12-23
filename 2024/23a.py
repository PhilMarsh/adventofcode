from collections import defaultdict
import itertools


def main():
    connection_pairs = _load_connection_pairs()

    adjacency_lookup = _build_adjacency_lookup(connection_pairs)
    trios = _yield_trio_cliques(adjacency_lookup)
    t_trios = [tri for tri in trios if any(c.startswith("t") for c in tri)]

    res = len(t_trios)
    print(res)


def _load_connection_pairs():
    with open("23.in") as file:
        return [x.strip().split("-") for x in file.readlines()]


def _build_adjacency_lookup(connection_pairs):
    lookup = defaultdict(set)
    for comp1, comp2 in connection_pairs:
        lookup[comp1].add(comp2)
        lookup[comp2].add(comp1)
    return dict(lookup)


def _yield_trio_cliques(adjacency_lookup):
    for comp1, adjacents in sorted(adjacency_lookup.items()):
        greater_adjacents = {c for c in adjacents if c > comp1}
        for comp2, comp3 in itertools.combinations(greater_adjacents, 2):
            if comp3 in adjacency_lookup[comp2]:
                yield (comp1, comp2, comp3)


if __name__ == "__main__":
    main()
