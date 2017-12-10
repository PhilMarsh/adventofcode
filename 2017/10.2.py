import operator
import sys

def sparse(lengths):
    values = list(range(256))
    pos = 0
    skip = 0
    for _ in range(64):
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

def condense_block(block):
    condensed = block[0]
    for num in block[1:]:
        condensed ^= num
    return condensed

def condense(sparse_hash):
    return [
        condense_block(block)
        for block in zip(*([iter(sparse_hash)] * 16))
    ]

def hexify(nums):
    return "".join(
        hex(n)[2:]
        for n in nums
    )

lengths = [
    ord(c)
    for c in sys.argv[1]
]
salt = [17, 31, 73, 47, 23]
sparse_hash = sparse(lengths + salt)
dense_hash = condense(sparse_hash)

print(hexify(dense_hash))
