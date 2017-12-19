import sys

grid = list(sys.stdin.readlines())

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

y = 0
x = grid[0].find("|")
dx, dy = DOWN

letters = []
while grid[y][x] != " ":
    x += dx
    y += dy
    cell = grid[y][x]
    if cell == "+":
        if dx:
            if grid[y-1][x] == "|":
                dx, dy = UP
            else:
                dx, dy = DOWN
        else:
            if grid[y][x-1] == "-":
                dx, dy = LEFT
            else:
                dx, dy = RIGHT
    elif cell.isalpha():
        letters.append(cell)
    # dont care about | and -

print("".join(letters))