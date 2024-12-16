from vector import Vector


_ROBOT = "@"
_WALL = "#"
_BOX_LEFT = "["
_BOX_RIGHT = "]"
_EMPTY = "."

_MOVE_DELTAS = {
    "^": Vector(x=0, y=-1),
    "v": Vector(x=0, y=1),
    "<": Vector(x=-1, y=0),
    ">": Vector(x=1, y=0),
}

_MAP_REMAPPINGS = (
    ("#", "##"),
    ("O", "[]"),
    (".", ".."),
    ("@", "@."),
)


def main():
    the_map, the_moves = _load_map_and_moves()

    robot_pos = _find_robot_pos(the_map)
    the_map[robot_pos.y][robot_pos.x] = _EMPTY

    final_map = _apply_moves(the_map, robot_pos, the_moves)

    res = sum(
        _gps_coordinate(y=y, x=x)
        for y, map_row in enumerate(final_map)
        for x, cell in enumerate(map_row)
        if cell == _BOX_LEFT
    )
    print(res)


def _load_map_and_moves():
    with open("15.in") as file:
        map_str, moves_str = file.read().split("\n\n")

    for symbol, double_symbol in _MAP_REMAPPINGS:
        map_str = map_str.replace(symbol, double_symbol)
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

        movable_connected = _select_movable_connected(
            the_map, pos=robot_pos, delta=delta
        )
        if movable_connected is None:
            continue

        # remove old places.
        for move_from_pos in movable_connected.keys():
            the_map[move_from_pos.y][move_from_pos.x] = _EMPTY
        # set new places.
        for move_from_pos, movable_val in movable_connected.items():
            move_to_pos = move_from_pos + delta
            the_map[move_to_pos.y][move_to_pos.x] = movable_val

        the_map[next_pos.y][next_pos.x] = _EMPTY  # current robot pos
        robot_pos = next_pos

    return the_map


def _select_movable_connected(the_map, *, pos, delta):
    connected = dict()
    last_connected = {pos: the_map[pos.y][pos.x]}
    while last_connected:
        new_connected = dict()
        for last_pos in last_connected.keys():
            new_pos = last_pos + delta
            new_val = the_map[new_pos.y][new_pos.x]
            if new_val == _WALL:
                return None
            elif new_val == _EMPTY:
                continue

            new_connected[new_pos] = new_val

            if new_val == _BOX_LEFT:
                other_box_pos = new_pos + Vector(x=1, y=0)
            else:
                assert new_val == _BOX_RIGHT
                other_box_pos = new_pos + Vector(x=-1, y=0)

            if other_box_pos != last_pos:
                new_connected[other_box_pos] = the_map[other_box_pos.y][other_box_pos.x]

        connected.update(new_connected)
        last_connected = new_connected

    return connected


def _gps_coordinate(*, y, x):
    return y * 100 + x


if __name__ == "__main__":
    main()
