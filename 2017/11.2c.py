import sys

DIRECTION_VECTOR_LOOKUP = {
    "n": (0, 1),
    "s": (0, -1),
    "ne": (1, 1),
    "sw": (-1, -1),
    "se": (1, 0),
    "nw": (-1, 0)
}

def hex_vector_magnitude(x, y):
    ne = 0
    if x > 0 and y > 0:
        ne = min(x, y)
    elif x < 0 and y < 0:
        ne = max(x, y)
    x -= ne
    y -= ne
    return abs(x) + abs(y) + abs(ne)

def hex_dist(path):
    x, y = (0, 0)
    max_dist = None

    for step in path:
        dx, dy = DIRECTION_VECTOR_LOOKUP[step]
        x += dx
        y += dy
        dist = hex_vector_magnitude(x, y)
        if max_dist is None or dist > max_dist:
            max_dist = dist

    return dist, max_dist

steps = sys.argv[1].split(",")
dist, max_dist = hex_dist(steps)

print(max_dist)
