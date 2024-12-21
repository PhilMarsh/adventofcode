from vector import Vector


_START = "S"
_END = "E"
_WALL = "#"
_TRACK = "."

_NORTH = Vector(x=0, y=-1)
_SOUTH = Vector(x=0, y=1)
_WEST = Vector(x=-1, y=0)
_EAST = Vector(x=1, y=0)
_ALL_DIRECTIONS = (_NORTH, _SOUTH, _WEST, _EAST)


def main():
    maze_lines = _load_input()
    maze_dict = {
        Vector(x=x, y=y): cell
        for y, row_line in enumerate(maze_lines)
        for x, cell in enumerate(row_line)
    }

    start_pos, end_pos = _pop_maze_start_and_end(maze_dict)
    track_list = list(_yield_track_positions(maze_dict, start_pos, end_pos))

    shortcut_times = dict(_yield_shortcut_items(maze_dict, track_list))

    res = sum(1 for time_saved in shortcut_times.values() if time_saved >= 100)
    print(res)


def _load_input():
    with open("20.in") as file:
        return [s.strip() for s in file.readlines()]


def _pop_maze_start_and_end(maze_dict):
    start = None
    end = None
    for pos, cell in maze_dict.items():
        if cell == _START:
            start = pos
        elif cell == _END:
            end = pos

    assert start and end
    maze_dict[start] = _TRACK
    maze_dict[end] = _TRACK

    return (start, end)


def _yield_track_positions(maze_dict, start_pos, end_pos):
    pos = start_pos
    direction = Vector(0, 0)
    while pos != end_pos:
        yield pos

        for next_direction in _ALL_DIRECTIONS:
            if next_direction == -direction:
                continue
            next_pos = pos + next_direction
            if maze_dict.get(next_pos) == _TRACK:
                pos = next_pos
                direction = next_direction
                # technically there will only ever be one matching direction,
                # but it doesn't hurt to end the search explicitly.
                break
    yield pos


def _yield_shortcut_items(maze_dict, track_list):
    track_indexes = {pos: i for i, pos in enumerate(track_list)}

    for start in track_list:
        assert maze_dict[start] == _TRACK
        for start_direction in _ALL_DIRECTIONS:
            wall = start + start_direction
            if maze_dict.get(wall) != _WALL:
                continue
            for end_direction in _ALL_DIRECTIONS:
                end = wall + end_direction
                if maze_dict.get(end) != _TRACK:
                    continue
                jump = track_indexes[end] - track_indexes[start] - 1
                saved = jump - 1
                if saved > 0:
                    assert (end - start).manhattan() == 2
                    yield ((start, end), saved)


if __name__ == "__main__":
    main()
