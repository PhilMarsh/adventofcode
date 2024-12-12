import dataclasses


def main():
    garden = _load_input()

    regions = _yield_regions(garden)

    res = sum(reg.area * reg.sides for reg in regions)
    print(res)


def _load_input():
    with open("12.in") as file:
        return [x.strip() for x in file.readlines()]


@dataclasses.dataclass
class _Region:
    area: int
    sides: int

    def __add__(self, other):
        return type(self)(
            area=self.area + other.area,
            sides=self.sides + other.sides,
        )


def _yield_regions(garden):
    visited = set()
    for y, garden_row in enumerate(garden):
        for x in range(len(garden_row)):
            if (y, x) not in visited:
                yield _flood_region(garden, y=y, x=x, visited=visited)


def _flood_region(garden, *, y, x, visited):
    visited.add((y, x))

    value = garden[y][x]
    region = _Region(area=1, sides=0)

    # each vertex (+) touches 4 cells:
    # 1 | 2
    # - + -
    # 3 | 4
    #
    # for a west-side fence:
    # - let quandrant 4 be (y, x).
    # - quandrant 3 is the other side of the fence.
    # - quandrants 1 and 2 decide whether the fence terminates at (y, x).
    #
    # travelling northward, there are 4 distinct cases for a west-side fence of
    # quandrant 4:
    #   no fence    turn right  straight    turn left
    #    1 ? 3       1 ? 2       1 | 2       1   2
    #    ? + ?       ? + -       ? +         - +
    #    3   4       3 | 4       3 | 4       3 | 4
    #
    # if there is no fence, then there is no side to count. if the fence
    # continues north, then it spans multiple cells and we can't yet uniquely
    # identify this side. but if the fence turns, then we know where a specific
    # end of this side is, and we can uniquely identify the side for counting.
    #
    # first, to have a fence at all, 3 and 4 must be different.
    # then, to turn, either (a) 2 and 4 must be different (turn right) or (b)
    # all of 1, 2, and 4 must be the same (turn left).
    #
    # we can rotate this pattern for all 4 cardinal directions, so sides in each
    # direction can be uniquely identified by the turn orientation.
    # thus we identify west sides by their northern ends, north sides by their
    # eastern ends, east sides by southern ends, south sides by western ends.

    for (row3, col3), (row1, col1), (row2, col2) in (
        ((y - 1, x), (y - 1, x + 1), (y, x + 1)),  # north side
        ((y + 1, x), (y + 1, x - 1), (y, x - 1)),  # south side
        ((y, x - 1), (y - 1, x - 1), (y - 1, x)),  # west side
        ((y, x + 1), (y + 1, x + 1), (y + 1, x)),  # east side
    ):
        if _garden_cell(garden, y=row3, x=col3) != value:
            if (
                _garden_cell(garden, y=row2, x=col2) != value
                or _garden_cell(garden, y=row1, x=col1) == value
            ):
                region.sides += 1
        elif (row3, col3) not in visited:
            region += _flood_region(garden, y=row3, x=col3, visited=visited)

    return region


def _garden_cell(garden, *, y, x):
    if y < 0 or y >= len(garden):
        return None
    garden_row = garden[y]
    if x < 0 or x >= len(garden_row):
        return None
    return garden_row[x]


if __name__ == "__main__":
    main()
