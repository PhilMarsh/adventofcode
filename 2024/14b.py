import dataclasses
import re

from vector import Vector


_ROBOT_REGEX = re.compile(r"p=(?P<x>-?\d+),(?P<y>-?\d+) v=(?P<dx>-?\d+),(?P<dy>-?\d+)")


_ROOM_WIDTH = 101
_ROOM_HEIGHT = 103


def main():
    robots = _load_robots()

    for t in range(10000):
        robot_positions = {_robot_after(bot, t).pos for bot in robots}
        picture = "\n".join(
            "".join(
                "*" if Vector(x=x, y=y) in robot_positions else " "
                for x in range(_ROOM_WIDTH)
            )
            for y in range(_ROOM_HEIGHT)
        )
        if ("*" * 10) in picture:
            print(f"\n\n    {t=}")
            print(picture)


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
            x=pos_after.x % _ROOM_WIDTH,
            y=pos_after.y % _ROOM_HEIGHT,
        ),
        vel=robot.vel,
    )


if __name__ == "__main__":
    main()
