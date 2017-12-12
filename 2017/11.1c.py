import sys

DIRECTION_VECTOR_LOOKUP = {
    "n": (0, 1),
    "s": (0, -1),
    "ne": (1, 1),
    "sw": (-1, -1),
    "se": (1, 0),
    "nw": (-1, 0)
}

def hex_dist(path):
    x, y = (0, 0)

    for step in path:
        dx, dy = DIRECTION_VECTOR_LOOKUP[step]
        x += dx
        y += dy

    ne = 0
    if x > 0 and y > 0:
        ne = min(x, y)
    elif x < 0 and y < 0:
        ne = max(x, y)
    x -= ne
    y -= ne

    return (
        abs(x)
        + abs(y)
        + abs(ne)
    )

steps = sys.argv[1].split(",")

print(hex_dist(steps))
