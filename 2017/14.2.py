from collections import deque
import sys

def sparse(lengths):
    values = list(range(256))
    pos = 0
    skip = 0
    for _ in range(64):
        for l in lengths:
            end = (pos + l) % len(values)
            if end < pos:
                elems = values[pos:] + values[:end]
            else:
                elems = values[pos:end]
            elems = list(reversed(elems))
            if end < pos:
                values[pos:] = elems[:len(values)-pos]
                values[:end] = elems[len(values)-pos:]
            else:
                values[pos:end] = elems
            pos = (pos + l + skip) % len(values)
            skip += 1
    return values

def condense_block(block):
    condensed = block[0]
    for num in block[1:]:
        condensed ^= num
    return condensed

def condense(sparse_hash):
    return [
        condense_block(block)
        for block in zip(*([iter(sparse_hash)] * 16))
    ]

def knot(s):
    lengths = [
        ord(c)
        for c in s
    ]
    salt = [17, 31, 73, 47, 23]
    sparse_hash = sparse(lengths + salt)
    return condense(sparse_hash)

def knot_bits(s):
    k = knot(s)
    return [
        0 if c == "0" else 1
        for n in k
        for c in "{0:08b}".format(n)
    ]

def regionify(grid):
    regioned_grid = [[0]*128]*128
    seen = set()
    region = 1
    for x in range(128):
        for y in range(128):
            if not grid[x][y]:
                continue
            if (x, y) in seen:
                continue
            # basically, dijkstra's algorithm?
            seen.add((x, y))
            queue = deque([(x, y)])
            while queue:
                (i, j) = queue.popleft()
                regioned_grid[i][j] = region
                if i > 0 and grid[i-1][j] and (i-1, j) not in seen:
                    seen.add((i-1, j))
                    queue.append((i-1, j))
                if j > 0 and grid[i][j-1] and (i, j-1) not in seen:
                    seen.add((i, j-1))
                    queue.append((i, j-1))
                if i < 127 and grid[i+1][j] and (i+1, j) not in seen:
                    seen.add((i+1, j))
                    queue.append((i+1, j))
                if j < 127 and grid[i][j+1] and (i, j+1) not in seen:
                    seen.add((i, j+1))
                    queue.append((i, j+1))
            region += 1
    return regioned_grid, region-1

key = sys.argv[1]
grid = [
    knot_bits("-".join((key, str(i))))
    for i in range(128)
]
regioned_grid, regions = regionify(grid)
print(regions)