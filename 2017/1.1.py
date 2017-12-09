import sys

def yield_digit_dups(s):
    for a, b in zip(s, s[1:]+s[:1]):
        if a == b:
            yield int(a)

print(sum(yield_digit_dups(sys.argv[1])))
