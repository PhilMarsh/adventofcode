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
            n += 1
        elif step == "s":
            n -= 1
        elif step == "ne":
            ne += 1
        elif step == "se":
            se += 1
        elif step == "nw":
            se -= 1
        elif step == "sw":
            ne -= 1

        # this feels very inefficent;
        # should be able to optimize based on current step.
        # was try-harding too much to figure out the elegant solution.
        if ne < 0 and se > 0:
            less_n = min(-ne, se)
            n -= less_n
            ne += less_n
            se -= less_n
        elif ne > 0 and se < 0:
            more_n = min(ne, -se)
            n += more_n
            ne -= more_n
            se += more_n

        if n < 0 and se < 0:
            less_ne = min(-n, -se)
            ne -= less_ne
            n += less_ne
            se += less_ne
        elif n > 0 and se > 0:
            more_ne = min(n, se)
            ne += more_ne
            n -= more_ne
            se -= more_ne

        if n > 0 and ne < 0:
            less_se = min(n, -ne)
            se -= less_se
            n -= less_se
            ne += less_se
        elif n < 0 and ne > 0:
            more_se = min(-n, ne)
            se += more_se
            n += more_se
            ne -= more_se

        dist = abs(n) + abs(ne) + abs(se)
        if max_dist is None or dist > max_dist:
            max_dist = dist

    return dist, max_dist

steps = list(sys.argv[1].split(","))
dist, max_dist = hex_dist(steps)
print(max_dist)
