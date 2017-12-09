import sys

def yield_min_max_diff(sheet):
    for row in sheet:
        yield (max(row) - min(row))

sheet = [
    [
        int(cell) 
        for cell in row.split()
    ]
    for row in sys.argv[1].splitlines()
]

print(sum(yield_min_max_diff(sheet)))
