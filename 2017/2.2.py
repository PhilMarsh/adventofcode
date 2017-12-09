import itertools
import sys

def yield_sole_int_quotients(sheet):
    for row in sheet:
        for a, b in itertools.combinations(row, 2):
            if a % b == 0:
                yield int(a/b)
                break
            if b % a == 0:
                yield int(b/a)
                break

sheet = [
    [
        int(cell) 
        for cell in row.split()
    ]
    for row in sys.argv[1].splitlines()
]

print(sum(yield_sole_int_quotients(sheet)))
