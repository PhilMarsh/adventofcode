import itertools
import sys

BASE_VECTORS = [
    (1, 0), # right
    (0, 1), # up
    (-1, 0), # left
    (0, -1) # down
]
def gen_vectors():
    """
        right 1,
        up 1,
        left 2,
        down 2,
        right 3,
        up 3,
        left 4,
        down 4,
        ...
    """
    vector_cycle = itertools.cycle(BASE_VECTORS)
    for k in itertools.count(1):
        # right/left
        yield from k * [next(vector_cycle)]
 
        # up/down
        yield from k * [next(vector_cycle)]

ADJ_VECTORS = [
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1)
]

def gen_adj_values(grid, x, y):
    for dx, dy in ADJ_VECTORS:
        yield grid.get((x + dx, y + dy), 0)

def find_first_adj_sum_larger_than(val):
    x, y = (0, 0)
    grid = {
        (x, y): 1
    }
    for dx, dy in gen_vectors():
        x += dx
        y += dy
        cell = sum(gen_adj_values(grid, x, y))
        if cell > val:
            return cell
        grid[(x, y)] = cell

print(find_first_adj_sum_larger_than(int(sys.argv[1])))
