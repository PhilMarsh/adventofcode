from collections import defaultdict
import itertools


def main():
    connection_pairs = _load_connection_pairs()

    adjacency_lookup = _build_adjacency_lookup(connection_pairs)
    largest_clique = _find_largest_clique(adjacency_lookup)

    res = ",".join(sorted(largest_clique))
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


def _find_largest_clique(adjacency_lookup):
    max_clique = tuple()
    for comp1, adjacents in adjacency_lookup.items():
        for subset_size in range(len(adjacents), 0, -1):
            # "+1" because `comp1` is part of the potential new clique too.
            if subset_size + 1 <= len(max_clique):
                break
            for adjacent_subset in itertools.combinations(adjacents, subset_size):
                if _is_clique(adjacency_lookup, adjacent_subset):
                    max_clique = (comp1, *adjacent_subset)
                    break
    return max_clique


def _is_clique(adjacency_lookup, comps):
    return all(
        c2 in adjacency_lookup[c1] for c1, c2 in itertools.combinations(comps, 2)
    )


if __name__ == "__main__":
    main()
