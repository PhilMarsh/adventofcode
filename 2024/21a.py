from vector import Vector


_UP = "^"
_DOWN = "v"
_LEFT = "<"
_RIGHT = ">"
_ACTIVATE = "A"

_ARROWPAD_BLANK_CORNER = Vector(x=0, y=0)
_ARROWPAD_SYMBOL_POSITIONS = {
    # blank: Vector(x=0, y=0),
    _UP: Vector(x=1, y=0),
    _ACTIVATE: Vector(x=2, y=0),
    _LEFT: Vector(x=0, y=1),
    _DOWN: Vector(x=1, y=1),
    _RIGHT: Vector(x=2, y=1),
}

_NUMPAD_BLANK_CORNER = Vector(x=0, y=3)
_NUMPAD_SYMBOL_POSITIONS = {
    "7": Vector(x=0, y=0),
    "8": Vector(x=1, y=0),
    "9": Vector(x=2, y=0),
    "4": Vector(x=0, y=1),
    "5": Vector(x=1, y=1),
    "6": Vector(x=2, y=1),
    "1": Vector(x=0, y=2),
    "2": Vector(x=1, y=2),
    "3": Vector(x=2, y=2),
    # blank: Vector(x=0, y=3),
    "0": Vector(x=1, y=3),
    _ACTIVATE: Vector(x=2, y=3),
}


def main():
    numpad_codes = _load_input()

    arrowpad_commands = [
        _arrowpad_commands_for_numpad_code(code, target_arrowpad_depth=2)
        for code in numpad_codes
    ]

    complexity_scores = [
        len(cmd) * _numpad_code_int(code)
        for cmd, code in zip(arrowpad_commands, numpad_codes)
    ]

    res = sum(complexity_scores)
    print(res)


def _load_input():
    with open("21.in") as file:
        return [x.strip() for x in file.readlines()]


def _arrowpad_commands_for_numpad_code(code, target_arrowpad_depth):
    return "".join(
        _best_numpad_move(start, end, target_arrowpad_depth)
        for start, end in zip(f"A{code}", code)
    )


def _arrowpad_commands_for_arrowpad_command(command, target_depth, depth=0):
    if depth == target_depth:
        return command

    return "".join(
        _best_arrowpad_move(start, end, target_depth, depth + 1)
        for start, end in zip(f"A{command}", command)
    )


def _best_numpad_move(start_symbol, end_symbol, target_arrowpad_depth):
    base_arrowpad_options = _numpad_move_options(start_symbol, end_symbol)
    full_arrowpad_options = [
        _arrowpad_commands_for_arrowpad_command(cmd, target_arrowpad_depth)
        for cmd in base_arrowpad_options
    ]
    return _shortest_command(full_arrowpad_options)


def _best_arrowpad_move(start_symbol, end_symbol, target_depth, depth):
    base_arrowpad_options = _arrowpad_move_options(start_symbol, end_symbol)
    full_arrowpad_options = [
        _arrowpad_commands_for_arrowpad_command(cmd, target_depth, depth)
        for cmd in base_arrowpad_options
    ]
    return _shortest_command(full_arrowpad_options)


def _numpad_move_options(start_symbol, end_symbol):
    start_pos = _NUMPAD_SYMBOL_POSITIONS[start_symbol]
    end_pos = _NUMPAD_SYMBOL_POSITIONS[end_symbol]
    return _pad_move_options_avoid_corner(start_pos, end_pos, _NUMPAD_BLANK_CORNER)


def _arrowpad_move_options(start_symbol, end_symbol):
    start_pos = _ARROWPAD_SYMBOL_POSITIONS[start_symbol]
    end_pos = _ARROWPAD_SYMBOL_POSITIONS[end_symbol]
    return _pad_move_options_avoid_corner(start_pos, end_pos, _ARROWPAD_BLANK_CORNER)


def _pad_move_options_avoid_corner(start_pos, end_pos, bad_corner_pos):
    delta = end_pos - start_pos
    moves = ""

    if delta.x > 0:
        h_moves = _RIGHT * delta.x
    elif delta.x < 0:
        h_moves = _LEFT * -delta.x
    else:
        h_moves = ""

    if delta.y < 0:
        v_moves = _UP * -delta.y
    elif delta.y > 0:
        v_moves = _DOWN * delta.y
    else:
        v_moves = ""

    if not h_moves:
        move_options = (v_moves,)
    elif not v_moves:
        move_options = (h_moves,)
    else:
        move_options = tuple()
        if start_pos.x != bad_corner_pos.x or end_pos.y != bad_corner_pos.y:
            move_options += (v_moves + h_moves,)

        if end_pos.x != bad_corner_pos.x or start_pos.y != bad_corner_pos.y:
            move_options += (h_moves + v_moves,)

    return [f"{opt}A" for opt in move_options]


def _numpad_code_int(code):
    return int(code[:-1])


def _shortest_command(commands):
    commands = set(commands)
    # command_sizes = dict()
    # for cmd in commands:
    #     command_sizes.setdefault(len(cmd), [])
    #     command_sizes[len(cmd)].append(cmd)
    # # command_sizes = {cmd: len(cmd) for cmd in commands}
    # print(f"{len(commands)=}\n{command_sizes=}")

    return sorted(commands, key=lambda c: (len(c), c))[0]


if __name__ == "__main__":
    main()
