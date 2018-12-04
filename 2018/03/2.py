import sys
from collections import defaultdict

grid = defaultdict(lambda: defaultdict(set))
clean_ids = set()
for claim in sys.stdin.read().strip().split("\n"):
    cid, _, xy, wh = claim.split(" ")
    x, y = xy.split(",")
    w, h = wh.split("x")
    x = int(x)
    y = int(y[:-1])
    w = int(w)
    h = int(h)

    clean_ids.add(cid)
    for xi in range(x, x+w):
        for yi in range(y, y+h):
            grid[xi][yi].add(cid)
            if len(grid[xi][yi]) > 1:
                clean_ids -= grid[xi][yi]

print(clean_ids)
