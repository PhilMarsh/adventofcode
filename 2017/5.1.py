import sys

def find_exit(offsets):
    i = 0
    steps = 0
    offsets = list(offsets)
    while i >= 0 and i < len(offsets):
        di = offsets[i]
        offsets[i] += 1
        i += di
        steps += 1
    return steps

offsets = [
    int(line)
    for line in sys.argv[1].splitlines()
]

print(find_exit(offsets))
