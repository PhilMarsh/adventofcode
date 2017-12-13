import sys

def severity(lines):
    severity = 0
    for l in lines:
        depth, size = l.split(": ")
        depth = int(depth)
        size = int(size)
        cycle = (size *  2) - 2
        if depth % cycle == 0:
            severity += depth * size
    return severity

print(severity(sys.stdin))