import sys
from collections import defaultdict

data = sys.stdin.read().strip("\n").split("\n")
points = list(
    tuple((int(x) for x in p.split(", ")))
    for p in data
)

min_x = min(x for x,y in points)
min_y = min(y for x,y in points)
max_x = max(x for x,y in points)
max_y = max(y for x,y in points)

grid = defaultdict(lambda: defaultdict(int))
for x in range(min_x-21, max_x+22):
    for y in range(min_y-21, max_y+22):
        for i, (px, py) in enumerate(points):
            dist = abs(x-px) + abs(y-py)
            grid[x][y] += dist

print(
    "\n".join(
        "".join(" {0:5} ".format(grid[x][y]) for x in range(min_x-21, max_x+22))
        for y in range(min_y-21, max_y+22)
    )
)

size = sum(
    1
    for x, col in grid.items()
    for y, cell in col.items()
    if cell < 10000
)

print(size)
