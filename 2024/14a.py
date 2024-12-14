import dataclasses
import re

from vector import Box, Vector


_ROBOT_REGEX = re.compile(r"p=(?P<x>-?\d+),(?P<y>-?\d+) v=(?P<dx>-?\d+),(?P<dy>-?\d+)")

# boxes edges are inclusive.
_Q1_BOUNDS = Box(Vector(0, 0), Vector(49, 50))
_Q2_BOUNDS = Box(Vector(51, 0), Vector(100, 50))
_Q3_BOUNDS = Box(Vector(0, 52), Vector(49, 102))
_Q4_BOUNDS = Box(Vector(51, 52), Vector(100, 102))

_QUANDRANTS = (
    _Q1_BOUNDS,
    _Q2_BOUNDS,
    _Q3_BOUNDS,
    _Q4_BOUNDS,
)


def main():
    robots = _load_robots()

    robots_after = [_robot_after(bot, 100) for bot in robots]

    score = 1
    for quad in _QUANDRANTS:
        count = 0
        for bot in robots_after:
            if bot.pos in quad:
                count += 1
        score *= count

    print(score)


def _load_robots():
    with open("14.in") as file:
        return [_parse_robot(line.strip()) for line in file.readlines()]


@dataclasses.dataclass(frozen=True)
class _Robot:
    pos: Vector
    vel: Vector


def _parse_robot(robot_str):
    match = _ROBOT_REGEX.match(robot_str)
    return _Robot(
        pos=Vector(
            x=int(match.group("x")),
            y=int(match.group("y")),
        ),
        vel=Vector(
            x=int(match.group("dx")),
            y=int(match.group("dy")),
        ),
    )


def _robot_after(robot, t):
    pos_after = robot.pos + robot.vel * t

    return _Robot(
        pos=Vector(
            x=pos_after.x % (_Q4_BOUNDS.max.x + 1),
            y=pos_after.y % (_Q4_BOUNDS.max.y + 1),
        ),
        vel=robot.vel,
    )


if __name__ == "__main__":
    main()
