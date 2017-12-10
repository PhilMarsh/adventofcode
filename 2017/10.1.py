import sys

def knot(lengths):
    values = list(range(256))
    pos = 0
    skip = 0
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

knotted = knot(
    int(num)
    for num in sys.argv[1].split(",")
)
print(knotted[0] * knotted[1])
