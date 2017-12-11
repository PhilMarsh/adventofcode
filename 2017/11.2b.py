import collections
import itertools
import sys

def hex_dist(path):
    n = 0
    ne = 0
    se = 0
    max_dist = None

    for step in path:
        if step == "n":
            if (se > 0 and ne < 0) or (n >= 0 and (se > 0 or ne < 0)):
                se -= 1
                ne += 1
            else:
                n += 1
        elif step == "s":
            if (se < 0 and ne > 0) or (n <= 0 and (se < 0 or ne > 0)):
                se += 1
                ne -= 1
            else:
                n -= 1
        elif step == "ne":
            if (n < 0  and se < 0) or (ne >= 0 and (n < 0 or se < 0)):
                n += 1
                se += 1
            else:
                ne += 1
        elif step == "sw":
            if (n > 0 and se > 0) or (ne <= 0 and (n > 0 or se > 0)):
                n -= 1
                se -= 1
            else:
                ne -= 1
        elif step == "se":
            if (n > 0 and ne > 0) or (se >= 0 and (n > 0 or ne < 0)):
                n -= 1
                ne += 1
            else:
                se += 1
        elif step == "nw":
            if (n < 0 and ne > 0) or (se <= 0 and (n < 0 or ne > 0)):
                n += 1
                ne -= 1
            else:
                se -= 1
        dist = abs(n) + abs(ne) + abs(se)
        if max_dist is None or dist > max_dist:
            max_dist = dist

    return dist, max_dist

steps = sys.argv[1].split(",")
dist, max_dist = hex_dist(steps)

print(max_dist)
