import sys
from collections import defaultdict

data = sys.stdin.read().strip("\n").split("\n")
#print(data)
#print(data[0])
#print(data[0].split(", "))
#print(data[-1].split(", "))

points = list()
for p in data:
    #print(p)
    x, y = p.split(", ")
    #print(x, y)
    points.append((int(x), int(y)))

#points = list(
#    (int(x), int(y))
#    for p in data
#    for x, y in p.split(", ", 1)
#)

min_x = min(x for x,y in points)
min_y = min(y for x,y in points)
max_x = max(x for x,y in points)
max_y = max(y for x,y in points)

grid = defaultdict(lambda: defaultdict(lambda: (None, (None, None))))
for x in range(min_x-1000, max_x+1000):
    for y in range(min_y-1000, max_y+1000):
        for i, (px, py) in enumerate(points):
            dist = abs(x-px) + abs(y-py)
            if grid[x][y][0] is None or dist < grid[x][y][1]:
                grid[x][y] = (i, dist)
            elif dist == grid[x][y][1]:
                grid[x][y] = (-1, dist)

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
        " ".join("{0:2}".format(grid[x][y][0]) for x in range(min_x-100, max_x+100))
        for y in range(min_y-100, max_y+100)
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
        "D" if i in disqualified else "OK"
    )
    for i in range(len(points))
    #if i not in disqualified
]

print(sorted(counts))
