from heap import MinHeap
from vector import Vector


_WALL = "#"
_START = "S"
_END = "E"
_EMPTY = "."

_MOVE_COST = 1
_TURN_COST = 1000

_NORTH = Vector(x=0, y=-1)
_SOUTH = Vector(x=0, y=1)
_WEST = Vector(x=-1, y=0)
_EAST = Vector(x=1, y=0)


def main():
    maze = _load_maze()

    maze_dict = dict(_yield_maze_items(maze))
    start_pos = _find_key(maze_dict, _START)
    end_pos = _find_key(maze_dict, _END)
    maze_dict[start_pos] = _EMPTY
    maze_dict[end_pos] = _EMPTY

    min_score, _ = _min_maze_score_and_path(
        maze_dict, pos=start_pos, direction=_EAST, target_pos=end_pos
    )

    print(min_score)


def _load_maze():
    with open("16.in") as file:
        return [list(line.strip()) for line in file.readlines()]


def _yield_maze_items(maze):
    for y, maze_row in enumerate(maze):
        for x, cell in enumerate(maze_row):
            yield Vector(x=x, y=y), cell


def _find_key(d, value):
    for key, val in d.items():
        if val == value:
            return key

    raise Exception(f"No '{value}'.")


def _min_maze_score_and_path(maze_dict, *, pos, direction, target_pos):
    seen_scores_and_paths = dict()
    todo = MinHeap(items=((0, pos, direction, tuple()),))
    while todo:
        score, pos, direction, path = todo.pop()

        old_score_and_path = seen_scores_and_paths.get(pos)
        if old_score_and_path is not None and old_score_and_path[0] < score:
            continue

        seen_scores_and_paths[pos] = (score, path)

        for next_direction in (_NORTH, _SOUTH, _WEST, _EAST):
            next_pos = pos + next_direction
            next_cell = maze_dict[next_pos]
            if next_cell == _WALL:
                continue

            next_path = path + (next_pos,)
            next_score = score + _MOVE_COST
            if next_direction != direction:
                next_score += _TURN_COST

            todo.push((next_score, next_pos, next_direction, next_path))

    return seen_scores_and_paths[target_pos]


if __name__ == "__main__":
    main()
