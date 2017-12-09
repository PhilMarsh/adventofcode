import sys

def yield_valid_phrases(phrases):
    for p in phrases:
        if len(p) == len(set(str(sorted(w)) for w in p)):
            yield p

phrases = [
    line.split()
    for line in sys.argv[1].splitlines()
]

print(sum(1 for _ in yield_valid_phrases(phrases)))
