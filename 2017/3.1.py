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

def find_position(index):
    x, y = (0, 0)
    i = 1
    for dx, dy in gen_vectors():
        if i == index:
            return (x, y)
        i += 1
        x += dx
        y += dy

def find_distance_from_center(index):
    x, y = find_position(index)
    return abs(x) + abs(y)

print(find_distance_from_center(int(sys.argv[1])))
