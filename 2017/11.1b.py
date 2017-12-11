import collections
import itertools
import sys

def hex_dist(path):
    n = 0
    ne = 0
    se = 0

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

    return (
        abs(n)
        + abs(ne)
        + abs(se)
    )

steps = sys.argv[1].split(",")

print(hex_dist(steps))
