# chased my tail on this one a bit.
# no idea what i was doing wrong last night, but suddenly after adding a bunch of debugging, and no logic changes (that i know of), my answer is correct.
# pretty sure it was the same answer as last night, but oh well.

# UPDATE:
#   "Because of a bug in the day 6 puzzle that made it unsolvable for some users until about two hours after unlock, day 6 is worth no points on the global leaderboard."
# i recovered my original from last night as og_1.py and re-ran it and i got the same (correct) answer. sigh.

import sys
from collections import defaultdict

data = sys.stdin.read().strip("\n").split("\n")
#print(data)
#print(data[0])
#print(data[0].split(", "))
#print(data[-1].split(", "))

#points = list()
#for p in data:
#    #print(p)
#    x, y = p.split(", ")
#    #print(x, y)
#    points.append((int(x), int(y)))

points = list(
    tuple((int(x) for x in p.split(", ")))
    for p in data
)

min_x = min(x for x,y in points)
min_y = min(y for x,y in points)
max_x = max(x for x,y in points)
max_y = max(y for x,y in points)

grid = defaultdict(lambda: defaultdict(lambda: (None, None)))
for x in range(min_x-100, max_x+100):
    for y in range(min_y-100, max_y+100):
        for i, (px, py) in enumerate(points):
            dist = abs(x-px) + abs(y-py)
            if dist == 0:
                grid[x][y] = ("[{0:2}]".format(i), dist)
            elif grid[x][y][0] is None or dist < grid[x][y][1]:
                grid[x][y] = (i, dist)
            elif dist == grid[x][y][1]:
                grid[x][y] = (-1, dist)

# second attempt: algorithmically determine bounded regions.
bounded = set()
for i, (px, py) in enumerate(points):
    north = False
    east = False
    south = False
    west = False
    for j, (x, y) in enumerate(points):
        if j == i:
            continue
        dy = abs(y-py)
        dx = abs(x-px)
        if dy >= dx:
            if py > y:
                north = True
            else:
                south = True
        if dx >= dy:
            if px > x:
                west = True
            else:
                east = True
    if all((north, east, south, west)):
        bounded.add(i)

print(bounded)

# first attempt: cull regions that go off the visible grid.
# grid was inflated by 100 in each direction to improve chances of this hueristic working.
# turned out with my specific input, the inflation wasn't necessary.
# also, this ends up being a good check to see *if* you need to inflate your grid to fully
# encompass all bounded regions.
disqualified = set(
    cell[0] for y, cell in grid[min(grid)].items()
).union(
    cell[0] for y, cell in grid[max(grid)].items()
).union(
    col[min(col)][0] for x, col in grid.items()
).union(
    col[max(col)][0] for x, col in grid.items()
)

print(disqualified)

print(
    "\n".join(
        "".join(grid[x][y][0] if isinstance(grid[x][y][0], str) else " {0:2} ".format(grid[x][y][0]) for x in range(min_x, max_x+1))
        for y in range(min_y, max_y+1)
    )
)


counts = [
    (
        sum(
            1
            for x, col in grid.items()
            for y, cell in col.items()
            if cell[0] == i
        ),
        i,
        # even without inflating the grid, disqualified and bounded were mutually exclusive and covered all 50 input points (ie: no "DB" and no "-")
        ("DB" if i in disqualified and i in bounded else "D" if i in disqualified else "B" if i in bounded else "-")
    )
    for i in range(len(points))
    #if i not in disqualified
]

print(sorted(counts))
