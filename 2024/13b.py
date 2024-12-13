"""
got stuck down a dead-end in the equation solving. got unstuck by checking
KaraMartin's solution:
https://github.com/KaraMartin/AdventOfCode2024/blob/612b2cea9e3c8d46a26c1a2468f30f25de75940f/initial/13.py#L76

also thanks to Ganon11 for providing the example answer missing from the
prompt: 875318608908.
"""

import dataclasses
import re

from vector import Vector


_A_PRICE = 3
_B_PRICE = 1

_PRIZE_OFFSET = Vector(10_000_000_000_000, 10_000_000_000_000)

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
                prize_pos=_parse_prize_pos(prize_line) + _PRIZE_OFFSET,
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
        xp = a*dxa + b*dxb
        yp = a*dya + b*dyb

    solving for `a`:
        b = (xp - a*dxa) / dxb
          = (yp - a*dya) / dyb

        (xp - a*dxa) / dxb = (yp - a*dya) / dyb
        (xp - a*dxa) * dyb = (yp - a*dya) * dxb
        xp*dyb - a*dxa*dyb = yp*dxb - a*dya*dxb
        xp*dyb - yp*dxb = a*dxa*dyb - a*dya*dxb
        xp*dyb - yp*dxb = a * (dxa*dyb - dya*dxb)

        a = (xp*dyb - yp*dxb) / (dxa*dyb - dya*dxb)

    solving for `b` (same thing, just swap all `a` and `b`):
        a = (xp - b*dxb) / dxa
          = (yp - b*dyb) / dya

        (xp - b*dxb) / dxa = (yp - b*dyb) / dya
        (xp - b*dxb) * dya = (yp - b*dyb) * dxa
        xp*dya - b*dxb*dya = yp*dxa - b*dyb*dxa
        xp*dya - yp*dxa = b*dxb*dya - b*dyb*dxa
        xp*dya - yp*dxa = b * (dxb*dya - dyb*dxa)

        b = (xp*dya - yp*dxa) / (dxb*dya - dyb*dxa)
    """
    prize = machine.prize_pos
    da = machine.a_delta
    db = machine.b_delta

    # colinear is a problem.
    assert da.unit() != db.unit()
    assert da.unit() != prize.unit()
    assert db.unit() != prize.unit()

    a = (prize.x * db.y - prize.y * db.x) / (da.x * db.y - da.y * db.x)
    b = (prize.x * da.y - prize.y * da.x) / (db.x * da.y - db.y * da.x)

    if a % 1 == 0 and b % 1 == 0:
        return _A_PRICE * int(a) + _B_PRICE * int(b)
    else:
        return None


if __name__ == "__main__":
    main()
