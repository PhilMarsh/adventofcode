import dataclasses
import re

from vector import Box, Vector


_A_PRICE = 3
_B_PRICE = 1

_MAX_BUTTON_PRESSES = 100

_BUTTON_REGEX = re.compile(r"Button [AB]: X\+(?P<dx>\d+), Y\+(?P<dy>\d+)")
_PRIZE_REGEX = re.compile(r"Prize: X=(?P<x>\d+), Y=(?P<y>\d+)")


def main():
    machines = _load_machines()

    res = sum(cost for m in machines if (cost := _min_prize_cost(m)) is not None)

    print(res)


def _load_machines():
    with open("13.in") as file:
        machine_lines = (m.split("\n") for m in file.read().strip().split("\n\n"))
        return [
            _Machine(
                a_delta=_parse_button_delta(a_line),
                b_delta=_parse_button_delta(b_line),
                prize_pos=_parse_prize_pos(prize_line),
            )
            for a_line, b_line, prize_line in machine_lines
        ]


@dataclasses.dataclass(frozen=True)
class _Machine:
    a_delta: Vector
    b_delta: Vector
    prize_pos: Vector


def _parse_button_delta(button_str):
    match = _BUTTON_REGEX.match(button_str)
    return Vector(
        x=int(match.group("dx")),
        y=int(match.group("dy")),
    )


def _parse_prize_pos(prize_str):
    match = _PRIZE_REGEX.match(prize_str)
    return Vector(
        x=int(match.group("x")),
        y=int(match.group("y")),
    )


def _min_prize_cost(machine):
    """
    find smallest `c`:
        c = 3*a + 1*b
        x = a*dxa + b*dxb
        y = a*dya + b*dyb
    """

    b = min(
        machine.prize_pos.y // machine.b_delta.y,
        machine.prize_pos.x // machine.b_delta.x,
        _MAX_BUTTON_PRESSES,
    )
    a = 0
    bounds = Box(Vector(0, 0), machine.prize_pos)

    pos = a * machine.a_delta + b * machine.b_delta
    while True:
        while pos in bounds:
            if pos == machine.prize_pos:
                return _prize_cost(a, b)
            elif a == _MAX_BUTTON_PRESSES:
                # can't add any more A.
                return None
            else:
                a += 1
                pos += machine.a_delta

        while pos not in bounds:
            if pos == machine.prize_pos:
                return _prize_cost(a, b)
            elif b == 0:
                # can't subtract any more B.
                return None
            else:
                b -= 1
                pos -= machine.b_delta


def _prize_cost(a_count, b_count):
    return _A_PRICE * a_count + _B_PRICE * b_count


if __name__ == "__main__":
    main()
