import itertools
import re


# use lookahead so matched chars are not consumed, so overlapping matches can be found.
_XMAS_REGEX = re.compile("(?=XMAS|SAMX)")


def main():
    row_strs = _load_row_strs("04.in")

    res = sum(
        1
        for s in _yield_print(
            itertools.chain(
                row_strs,
                _yield_column_strs(row_strs),
                _yield_diagonal_strs_upper_right_triangle(row_strs),
                _yield_diagonal_strs_lower_left_triangle(row_strs),
                _yield_diagonal_strs_upper_left_triangle(row_strs),
                _yield_diagonal_strs_lower_right_triangle(row_strs),
            )
        )
        for _ in _XMAS_REGEX.finditer(s)
    )

    print(res)


def _yield_print(iterable):
    for index, val in enumerate(iterable):
        print(f"{index}: {val}")
        yield val


def _load_row_strs(filename):
    with open(filename) as file:
        return [s.strip() for s in file.readlines()]


def _yield_column_strs(row_strs):
    yield from _yield_across_rows(row_strs)


def _yield_diagonal_strs_upper_right_triangle(row_strs):
    #   \\\\    \\    \\\\
    #   .\\\    .\    .\\\
    #   ..\\    ..
    #   ...\    ..
    # include main diagonal from top-left.

    diag_strs = [row_strs[i][i:] for i in range(len(row_strs))]
    yield from _yield_across_rows(diag_strs)


def _yield_diagonal_strs_lower_right_triangle(row_strs):
    #   ....    ..    ....
    #   .../    ./    .../
    #   ..//    //
    #   .///    //
    # exclude main diagonal from top-right.

    num_cols = len(row_strs[0])
    diag_strs = [row_strs[i][num_cols - i :] for i in range(1, len(row_strs))]
    yield from _yield_across_rows(diag_strs)


def _yield_diagonal_strs_upper_left_triangle(row_strs):
    #   ////    //    ////
    #   ///.    /.    ///.
    #   //..    ..
    #   /...    ..
    # include main diagonal from top-right.

    # mirror the board and check from the other direction because it's easier
    # to align the fronts of strings, rather than the backs.
    reversed_row_strs = [s[::-1] for s in row_strs]
    yield from _yield_diagonal_strs_upper_right_triangle(reversed_row_strs)


def _yield_diagonal_strs_lower_left_triangle(row_strs):
    #   ....    ..    ....
    #   \...    \.    \...
    #   \\..    \\
    #   \\\.    \\
    # exclude main diagonal from top-left.

    # mirror the board and check from the other direction because it's easier
    # to align the fronts of strings, rather than the backs.
    reversed_row_strs = [s[::-1] for s in row_strs]
    yield from _yield_diagonal_strs_lower_right_triangle(reversed_row_strs)


def _yield_across_rows(row_strs):
    for column in itertools.zip_longest(*row_strs, fillvalue=""):
        yield "".join(column)


if __name__ == "__main__":
    main()
