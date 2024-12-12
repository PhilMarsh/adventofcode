import dataclasses


def main():
    garden = _load_input()

    regions = _yield_regions(garden)

    res = sum(reg.area * reg.perimeter for reg in regions)
    print(res)


def _load_input():
    with open("12.in") as file:
        return [x.strip() for x in file.readlines()]


@dataclasses.dataclass
class _Region:
    area: int
    perimeter: int

    def __add__(self, other):
        return type(self)(
            area=self.area + other.area,
            perimeter=self.perimeter + other.perimeter,
        )


def _yield_regions(garden):
    visited = set()
    for y, row in enumerate(garden):
        for x in range(len(row)):
            if (y, x) not in visited:
                yield _flood_region(garden, y=y, x=x, visited=visited)


def _flood_region(garden, *, y, x, visited):
    visited.add((y, x))

    value = garden[y][x]
    region = _Region(area=1, perimeter=0)

    for row, col in (
        (y - 1, x),  # north
        (y + 1, x),  # south
        (y, x - 1),  # west
        (y, x + 1),  # east
    ):
        if (
            row < 0
            or row >= len(garden)
            or col < 0
            or col >= len(garden[row])
            or garden[row][col] != value
        ):
            region.perimeter += 1
        elif (row, col) not in visited:
            region += _flood_region(garden, y=row, x=col, visited=visited)

    return region


if __name__ == "__main__":
    main()
