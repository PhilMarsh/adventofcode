"""
Backport Part 2 solution to Part 1. Same code, just different `_XMAS_PATTERNS` config.
"""

_ANY = object()
_XMAS_PATTERNS = (
    (
        ("X", "M", "A", "S"),
    ),
    (
        ("S", "A", "M", "X"),
    ),
    (
        ("X",),
        ("M",),
        ("A",),
        ("S",),
    ),
    (
        ("S",),
        ("A",),
        ("M",),
        ("X",),
    ),
    (
        ("X", _ANY, _ANY, _ANY),
        (_ANY, "M", _ANY, _ANY),
        (_ANY, _ANY, "A", _ANY),
        (_ANY, _ANY, _ANY, "S"),
    ),
    (
        ("S", _ANY, _ANY, _ANY),
        (_ANY, "A", _ANY, _ANY),
        (_ANY, _ANY, "M", _ANY),
        (_ANY, _ANY, _ANY, "X"),
    ),
    (
        (_ANY, _ANY, _ANY, "S"),
        (_ANY, _ANY, "A", _ANY),
        (_ANY, "M", _ANY, _ANY),
        ("X", _ANY, _ANY, _ANY),
    ),
    (
        (_ANY, _ANY, _ANY, "X"),
        (_ANY, _ANY, "M", _ANY),
        (_ANY, "A", _ANY, _ANY),
        ("S", _ANY, _ANY, _ANY),
    ),
)


def main():
    row_strs = _load_row_strs("04.in")

    res = sum(
        1
        for y in range(len(row_strs))
        for x in range(len(row_strs[0]))
        for pattern in _XMAS_PATTERNS
        if _matches_pattern(
            matrix=row_strs,
            base_y=y,
            base_x=x,
            pattern=pattern,
        )
    )

    print(res)


def _load_row_strs(filename):
    with open(filename) as file:
        return [s.strip() for s in file.readlines()]


def _matches_pattern(*, matrix, base_y, base_x, pattern):
    for pattern_y, pattern_row in enumerate(pattern):
        y = base_y + pattern_y
        for pattern_x, pattern_val in enumerate(pattern_row):
            x = base_x + pattern_x
            try:
                val = matrix[y][x]
            except IndexError:
                return False

            if pattern_val is not _ANY and val != pattern_val:
                return False
    return True


if __name__ == "__main__":
    main()
