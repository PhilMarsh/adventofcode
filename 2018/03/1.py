import sys
from collections import defaultdict

grid = defaultdict(lambda: defaultdict(set))

for claim in sys.stdin.read().strip().split("\n"):
    cid, _, xy, wh = claim.split(" ")
    x, y = xy.split(",")
    w, h = wh.split("x")
    x = int(x)
    y = int(y[:-1])
    w = int(w)
    h = int(h)

    for xi in range(x, x+w):
        for yi in range(y, y+h):
            grid[xi][yi].add(cid)

print(
    sum(
        1
        for col in grid.values()
        for cell in col.values()
        if len(cell) > 1
    )
)
