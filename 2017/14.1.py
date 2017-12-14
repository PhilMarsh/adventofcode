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

def knot(s):
    lengths = [
        ord(c)
        for c in s
    ]
    salt = [17, 31, 73, 47, 23]
    sparse_hash = sparse(lengths + salt)
    return condense(sparse_hash)

def knot_ones(s):
    k = knot(s)
    return sum(
        bin(n).count("1")
        for n in k
    )

key = sys.argv[1]
total_ones = sum(
    knot_ones("-".join((key, str(i))))
    for i in range(128)
)
print(total_ones)