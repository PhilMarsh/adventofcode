import sys

# top left is (0, 0)
DIRECTIONS = (
    (0, -1), # up
    (1, 0), # right
    (0, 1), # down
    (-1, 0) # left
)

infected = set()
base_grid_size = 0
for y, row in enumerate(sys.stdin.readlines()):
    base_grid_size += 1
    for x, cell in enumerate(row):
        if cell == "#":
            infected.add((x, y))

new_infections = 0

# start at the center
x = y = base_grid_size // 2
# start facing up
direction = 0

for _ in range(10000):
    if (x, y) in infected:
        direction = (direction+1) % 4 # turn right
        infected.remove((x, y))
    else:
        direction = (direction+3) % 4 # turn left
        infected.add((x, y))
        new_infections += 1
    dx, dy = DIRECTIONS[direction]
    x += dx
    y += dy

print(new_infections)