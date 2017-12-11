import collections
import itertools
import sys

def hex_dist(path):
    n = 0
    ne = 0
    se = 0

    for step in path:
        if step == "n":
            if se > 0 and ne < 0:
                se -= 1
                ne += 1
            else:
                n += 1
        elif step == "s":
            if n > 0:
                n -= 1
            else:
                se += 1
                ne -= 1
        elif step == "ne":
            if n < 0 and se < 0:
                n += 1
                se += 1
            else:
                ne += 1
        elif step == "se":
            if n > 0 and ne < 0:
                n -= 1
                ne += 1
            else:
                se += 1
        elif step == "nw":
            if se > 0:
                se -= 1
            else:
                n += 1
                ne -= 1
        elif step == "sw":
            if ne > 0:
                ne -= 1
            else:
                n -= 1
                se -= 1

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

    return (
        abs(n)
        + abs(ne)
        + abs(se)
    )

steps = list(sys.argv[1].split(","))

print(hex_dist(steps))
