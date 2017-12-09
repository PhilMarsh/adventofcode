import sys

def largest_bank(bank_sizes):
    largest_size = 0
    for i, size in bank_sizes.items():
        if size > largest_size:
            largest_i = i
            largest_size = size
    return largest_i, largest_size

def redist(bank_sizes):
    largest_i, largest_size = largest_bank(bank_sizes)
    num_banks = len(bank_sizes)
    shared = int(largest_size / num_banks)
    extra = largest_size % num_banks
    return {
        i: 
            (size if i != largest_i else 0)
            + shared
            + (1 if ((i + num_banks-largest_i-1) % num_banks) < extra else 0)
        for i, size in bank_sizes.items()
    }

def yield_redist_states(bank_sizes):
    bank_sizes = dict(enumerate(bank_sizes))
    while True:
        yield tuple(size for _, size in sorted(bank_sizes.items()))
        bank_sizes = redist(bank_sizes)

def num_until_repeat(iterable):
    count = 0
    seen = set()
    for val in iterable:
        if val in seen:
            return count
        seen.add(val)
        count += 1

bank_sizes = [
    int(size)
    for size in sys.argv[1].split()
]

print(num_until_repeat(yield_redist_states(bank_sizes)))
