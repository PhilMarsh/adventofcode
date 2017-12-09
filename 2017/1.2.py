import sys

def yield_digit_dups(s):
    dist = int(len(s)/2)
    for a, b in zip(s, s[dist:]+s[:dist]):
        if a == b:
            yield int(a)

print(sum(yield_digit_dups(sys.argv[1])))
