from vector import Vector


_ROBOT = "@"
_WALL = "#"
_BOX = "O"
_EMPTY = "."

_MOVE_DELTAS = {
    "^": Vector(x=0, y=-1),
    "v": Vector(x=0, y=1),
    "<": Vector(x=-1, y=0),
    ">": Vector(x=1, y=0),
}


def main():
    the_map, the_moves = _load_map_and_moves()

    robot_pos = _find_robot_pos(the_map)
    the_map[robot_pos.y][robot_pos.x] = _EMPTY

    final_map = _apply_moves(the_map, robot_pos, the_moves)

    res = sum(
        _gps_coordinate(y=y, x=x)
        for y, map_row in enumerate(final_map)
        for x, cell in enumerate(map_row)
        if cell == _BOX
    )
    print(res)


def _load_map_and_moves():
    with open("15.in") as file:
        map_str, moves_str = file.read().split("\n\n")
    the_map = [list(s) for s in map_str.split()]
    return the_map, moves_str.replace("\n", "")


def _find_robot_pos(the_map):
    for y, map_row in enumerate(the_map):
        for x, cell in enumerate(map_row):
            if cell == _ROBOT:
                return Vector(x=x, y=y)
    raise Exception(f"no robot: {the_map=}")


def _apply_moves(the_map, robot_pos, the_moves):
    the_map = [list(row) for row in the_map]
    for move in the_moves:
        delta = _MOVE_DELTAS[move]
        next_pos = robot_pos + delta

        next_non_box_pos, next_non_box_val = _find_next_non_box(
            the_map, pos=robot_pos, delta=delta
        )
        if next_non_box_val == _WALL:
            continue
        else:
            assert next_non_box_val == _EMPTY

        the_map[next_non_box_pos.y][next_non_box_pos.x] = _BOX
        the_map[next_pos.y][next_pos.x] = _EMPTY  # current robot pos
        robot_pos = next_pos

    return the_map


def _find_next_non_box(the_map, *, pos, delta):
    pos += delta
    while the_map[pos.y][pos.x] == _BOX:
        pos += delta
    return pos, the_map[pos.y][pos.x]


def _gps_coordinate(*, y, x):
    return y * 100 + x


if __name__ == "__main__":
    main()
