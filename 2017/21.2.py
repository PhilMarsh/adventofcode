import sys

def gen_alternates(grid):
    yield from gen_rotations(grid)
    flipped = flip(grid)
    yield from gen_rotations(flipped)

def gen_rotations(grid):
    yield grid
    rotated = grid
    for _ in range(3):
        rotated = rotate(rotated)
        yield rotated

def rotate(grid):
    # rotate 90 clockwise.
    # left column -> top row
    return [
        [
            grid[y][x]
            for y in range(len(grid)-1, 0-1, -1)
        ]
        for x in range(len(grid))
    ]

def flip(grid):
    # flip horizontal.
    # left column becomes right column
    return [
        list(reversed(row))
        for row in grid
    ]

def parse_grid(raw):
    return [
        [
            True if cell == "#" else False
            for cell in row
        ]
        for row in raw.split("/")
    ]

def str_grid(grid):
    return "/".join(
        "".join(
            "#" if cell else "."
            for cell in row
        )
        for row in grid
    )

def evolve(grid, rules):
    subgrid_size = 3
    if len(grid) % 2 == 0:
        subgrid_size = 2
    art = []
    for top in range(0, len(grid), subgrid_size):
        art_down = [[]] * (subgrid_size+1)
        for left in range(0, len(grid), subgrid_size):
            subgrid = extract_sub_grid(grid, top, left, subgrid_size)
            art_right = rules[str_grid(subgrid)]
            art_down = stitch_grid_right(art_down, art_right)
        art = stitch_grid_down(art, art_down)
    return art

def extract_sub_grid(grid, top, left, size):
    return [
        [
            grid[y][x]
            for x in range(left, left+size)
        ]
        for y in range(top, top+size)
    ]

def stitch_grid_right(base, right):
    return [
        base_row + right_row
        for base_row, right_row in zip(base, right)
    ]

def stitch_grid_down(base, down):
    return base + down

rules = dict()
for line in sys.stdin.readlines():
    raw_key, raw_val = line.strip().split(" => ")
    parsed_key = parse_grid(raw_key)
    parsed_val = parse_grid(raw_val)
    for alt_key in gen_alternates(parsed_key):
        rules[str_grid(alt_key)] = parsed_val

art = [
    [False, True, False],
    [False, False, True],
    [True, True, True]
]

for _ in range(18):
    print(_)#, "\n", str_grid(art).replace("/", "\n"))
    art = evolve(art, rules)

# print("\n\n", str_grid(art).replace("/", "\n"))
print(sum(1 if cell == "#" else 0 for cell in str_grid(art)))