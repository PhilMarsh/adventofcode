from heap import MinHeap
from vector import Box, Vector


_MAZE_WIDTH = 71
_MAZE_HEIGHT = 71

_MAZE_START = Vector(x=0, y=0)
_MAZE_END = Vector(x=_MAZE_WIDTH - 1, y=_MAZE_HEIGHT - 1)

_WALL = "#"
_EMPTY = "."

_NORTH = Vector(x=0, y=-1)
_SOUTH = Vector(x=0, y=1)
_WEST = Vector(x=-1, y=0)
_EAST = Vector(x=1, y=0)


def main():
    bad_spaces = _load_bad_spaces()

    min_bad_spaces = 1
    max_bad_spaces = len(bad_spaces)
    while min_bad_spaces < max_bad_spaces:
        num_bad_spaces = (max_bad_spaces + min_bad_spaces) // 2
        maze_dict = dict(_yield_maze_items(set(bad_spaces[:num_bad_spaces])))

        print(f"\n{min_bad_spaces=}, {max_bad_spaces=}, {num_bad_spaces=}")

        path = tuple()
        try:
            _, path = _min_maze_steps_and_paths(
                maze_dict, pos=_MAZE_START, target_pos=_MAZE_END
            )
        except _NoPath:
            print(f"fail")
            max_bad_spaces = num_bad_spaces
        else:
            print(f"pass")
            min_bad_spaces = num_bad_spaces + 1
        # finally:
        #     picture = "\n".join(
        #         "".join(
        #             "O" if Vector(x=x, y=y) in path else maze_dict[Vector(x=x, y=y)]
        #             for x in range(_MAZE_WIDTH)
        #         )
        #         for y in range(_MAZE_HEIGHT)
        #     )
        #     print(picture)

    assert min_bad_spaces == max_bad_spaces

    blocking_bad_space = bad_spaces[min_bad_spaces-1]
    print(f"{blocking_bad_space.x},{blocking_bad_space.y}")


def _load_bad_spaces():
    with open("18.in") as file:
        return [
            Vector(*(int(val) for val in line.strip().split(",")))
            for line in file.readlines()
        ]


def _yield_maze_items(bad_spaces):
    for y in range(_MAZE_HEIGHT):
        for x in range(_MAZE_WIDTH):
            vec = Vector(x=x, y=y)
            if vec in bad_spaces:
                cell = _WALL
            else:
                cell = _EMPTY
            yield vec, cell


class _NoPath(Exception):
    pass


def _min_maze_steps_and_paths(maze_dict, *, pos, target_pos):
    seen_steps_and_paths = dict()
    todo = MinHeap(items=(((target_pos - pos).manhattan(), 0, pos, (pos,)),))
    while todo:
        _, steps, pos, path = todo.pop()

        old_steps_and_path = seen_steps_and_paths.get(pos)
        if old_steps_and_path is None or steps < old_steps_and_path[0]:
            seen_steps_and_paths[pos] = (steps, path)
        else:
            continue

        if pos == target_pos:
            break

        for next_direction in (_NORTH, _SOUTH, _WEST, _EAST):
            next_pos = pos + next_direction
            if next_pos == path[-1]:
                # quick optimization: don't look back.
                continue

            next_cell = maze_dict.get(next_pos)
            if next_cell is None or next_cell == _WALL:
                continue

            next_path = path + (next_pos,)
            next_steps = steps + 1
            next_score = next_steps + (target_pos - next_pos).manhattan()

            todo.push((next_score, next_steps, next_pos, next_path))

    try:
        return seen_steps_and_paths[target_pos]
    except KeyError:
        raise _NoPath


if __name__ == "__main__":
    main()
