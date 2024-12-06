"""
optimize Part 2 by shrinking the search space to only the spaces of the
original walk. cut search space by ~75%, reducing runtime from ~70s to ~16s.
"""

import dataclasses
from enum import Enum


_OBSTACLE = "#"


class _Direction(Enum):
    UP = "^"
    DOWN = "v"
    RIGHT = ">"
    LEFT = "<"


@dataclasses.dataclass(frozen=True)
class _WalkResult:
    visited_space_ids: set[tuple[int, int, _Direction]]
    ended_in_a_loop: bool


def main():
    the_map = _load_map("06.in")

    guard_y, guard_x, _ = _find_guard_start(the_map)
    original_walk = _walk(the_map)
    assert not original_walk.ended_in_a_loop

    original_walk_coords = set((y, x) for y, x, _ in original_walk.visited_space_ids)
    loop_obstacle_spaces = [
        (y, x)
        for y, x in original_walk_coords
        if (y, x) != (guard_y, guard_x)
        and _walk(
            _map_plus_obstacle(
                original_map=the_map,
                new_obstacle_y=y,
                new_obstacle_x=x,
            )
        ).ended_in_a_loop
    ]

    print(len(loop_obstacle_spaces))


def _map_plus_obstacle(*, original_map, new_obstacle_y, new_obstacle_x):
    print(f"obstacle ({new_obstacle_y}, {new_obstacle_x})")
    new_map = [list(row) for row in original_map]
    new_map[new_obstacle_y][new_obstacle_x] = _OBSTACLE
    return new_map


def _walk(the_map):
    map_top = 0
    map_bottom = len(the_map) - 1
    map_left = 0
    map_right = len(the_map[0]) - 1

    guard_y, guard_x, guard_direction = _find_guard_start(the_map)
    visited_spaces = set()
    while True:
        space_id = (guard_y, guard_x, guard_direction)
        if space_id in visited_spaces:
            return _WalkResult(visited_spaces, ended_in_a_loop=True)
        else:
            visited_spaces.add(space_id)

        # debug
        # the_map[guard_y][guard_x] = guard_direction.value

        if guard_direction == _Direction.UP:
            if guard_y == map_top:
                break
            elif the_map[guard_y - 1][guard_x] == _OBSTACLE:
                guard_direction = _Direction.RIGHT
            else:
                guard_y -= 1

        elif guard_direction == _Direction.DOWN:
            if guard_y == map_bottom:
                break
            elif the_map[guard_y + 1][guard_x] == _OBSTACLE:
                guard_direction = _Direction.LEFT
            else:
                guard_y += 1

        elif guard_direction == _Direction.LEFT:
            if guard_x == map_left:
                break
            elif the_map[guard_y][guard_x - 1] == _OBSTACLE:
                guard_direction = _Direction.UP
            else:
                guard_x -= 1

        else:
            assert guard_direction == _Direction.RIGHT

            if guard_x == map_right:
                break
            elif the_map[guard_y][guard_x + 1] == _OBSTACLE:
                guard_direction = _Direction.DOWN
            else:
                guard_x += 1

    visited_spaces.add((guard_y, guard_x, guard_direction))

    # debug
    # print("\n".join(f"{i+1:03} " + "".join(row) for i, row in enumerate(the_map)))

    return _WalkResult(visited_spaces, ended_in_a_loop=False)


def _load_map(filename):
    with open(filename) as file:
        return [list(s.strip()) for s in file.readlines()]


def _find_guard_start(the_map):
    direction_values = {d.value for d in _Direction}
    guard_positions_and_directions = [
        (y, x, _Direction(cell))
        for y, row in enumerate(the_map)
        for x, cell in enumerate(row)
        if cell in direction_values
    ]
    assert len(guard_positions_and_directions) == 1, guard_positions_and_directions

    return guard_positions_and_directions[0]


if __name__ == "__main__":
    main()
