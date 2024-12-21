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

    shortcut_times = dict(
        _yield_shortcut_items(maze_dict, track_list, max_cheat_time=20)
    )

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


def _yield_shortcut_items(maze_dict, track_list, max_cheat_time):
    track_indexes = {pos: i for i, pos in enumerate(track_list)}

    for start_index, start_pos in enumerate(track_list):
        tracks_in_range = _yield_track_positions_in_range(
            maze_dict,
            max_dist=max_cheat_time,
            pos=start_pos,
        )
        for end_pos in tracks_in_range:
            end_index = track_indexes[end_pos]

            if end_index <= start_index:
                continue

            direct_delta = end_pos - start_pos
            direct_dist = direct_delta.manhattan()
            assert direct_dist <= max_cheat_time

            track_dist = end_index - start_index

            saved_dist = track_dist - direct_dist
            if saved_dist > 0:
                yield ((start_pos, end_pos), saved_dist)


def _yield_track_positions_in_range(maze_dict, max_dist, *, pos):
    for dy in range(-max_dist, max_dist + 1):
        max_x_dist = max_dist - abs(dy)
        for dx in range(-max_x_dist, max_x_dist + 1):
            diff = Vector(x=dx, y=dy)
            diff_pos = pos + diff
            cell = maze_dict.get(diff_pos)
            if cell == _TRACK:
                yield diff_pos


if __name__ == "__main__":
    main()
