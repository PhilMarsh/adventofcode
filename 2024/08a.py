from collections import defaultdict
import dataclasses
import itertools
import string


_FREQUENCY_CHARS = set(string.ascii_letters + string.digits)


@dataclasses.dataclass(frozen=True)
class _Vector:
    x: int
    y: int

    def __sub__(self, other):
        return _Vector(x=self.x - other.x, y=self.y - other.y)

    def __add__(self, other):
        return _Vector(x=self.x + other.x, y=self.y + other.y)


@dataclasses.dataclass(frozen=True)
class _Box:
    v1: _Vector
    v2: _Vector

    def __contains__(self, vector):
        return (
            self.v1.y <= vector.y <= self.v2.y or self.v1.y >= vector.y >= self.v2.y
        ) and (self.v1.x <= vector.x <= self.v2.x or self.v1.x >= vector.x >= self.v2.x)


def main():
    the_map = _load_map()

    bounding_box = _Box(
        _Vector(x=0, y=0), _Vector(x=len(the_map[0]) - 1, y=len(the_map) - 1)
    )
    freq_node_vectors = _collect_frequency_node_vectors(the_map)
    antinode_vectors = set(
        anti
        for nodes in freq_node_vectors.values()
        for anti in _yield_antinode_vectors(nodes, bounding_box)
    )

    res = len(antinode_vectors)

    print(res)


def _load_map():
    with open("08.in") as file:
        return [s.strip() for s in file.readlines()]


def _collect_frequency_node_vectors(the_map):
    freq_vectors = defaultdict(list)
    for y, row in enumerate(the_map):
        for x, val in enumerate(row):
            if val in _FREQUENCY_CHARS:
                freq_vectors[val].append(_Vector(x=x, y=y))
    return dict(freq_vectors)


def _yield_antinode_vectors(node_vectors, bounding_box):
    for v1, v2 in itertools.combinations(node_vectors, 2):
        delta = v2 - v1
        for anti_vec in (v1 - delta, v2 + delta):
            if anti_vec in bounding_box:
                yield anti_vec


if __name__ == "__main__":
    main()
