import itertools


_MIN_CELL_VALUE = 0
_MAX_CELL_VALUE = 9


def main():
    topo_map = _load_topo_map()

    trailheads = _yield_trailheads(topo_map)
    peak_path_sets = (set(_yield_peak_paths(topo_map, y=y, x=x)) for y, x in trailheads)
    res = sum(len(peak_paths) for peak_paths in peak_path_sets)
    print(res)


def _load_topo_map():
    with open("10.in") as file:
        return [[int(c) for c in s.strip()] for s in file.readlines()]


def _yield_trailheads(topo_map):
    for y, row in enumerate(topo_map):
        for x, cell in enumerate(row):
            if cell == _MIN_CELL_VALUE:
                yield (y, x)


def _yield_peak_paths(topo_map, *, y, x):
    cell_value = topo_map[y][x]
    path_prefix = ((y, x),)
    if cell_value == _MAX_CELL_VALUE:
        yield path_prefix
    else:
        suffix_paths = itertools.chain.from_iterable(
            _yield_peak_paths(topo_map, y=next_y, x=next_x)
            for next_y, next_x in _yield_adjacents(
                y=y, x=x, height=len(topo_map), width=len(topo_map[0])
            )
            if topo_map[next_y][next_x] == cell_value + 1
        )
        for suffix in suffix_paths:
            yield path_prefix + suffix


_VISITED = object()


def _yield_adjacents(*, y, x, height, width):
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i != j and i != -j:
                row = y + i
                col = x + j
                if 0 <= row < height and 0 <= col < width:
                    yield (y + i, x + j)


if __name__ == "__main__":
    main()
