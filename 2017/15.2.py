import itertools
import sys

def gen(start, factor, mod):
    prev = start
    while True:
        curr = (prev * factor) % 2147483647
        if curr % mod == 0:
            yield curr
        prev = curr

def get_low_16_bits(n):
    return n % (2**16)

def count_matches(a, b):
    count = 0
    for p, q, i in zip(a, b, itertools.count()):
        if i == 5000000:
            break
        if get_low_16_bits(p) == get_low_16_bits(q):
            count += 1
    return count

a = gen(int(sys.argv[1]), 16807, 4)
b = gen(int(sys.argv[2]), 48271, 8)

print(count_matches(a, b))