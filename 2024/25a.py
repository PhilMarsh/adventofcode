_EMPTY = "."
_FILLED = "#"

_MAX_HEIGHT = 5


def main():
    locks, keys = _load_locks_and_keys()

    valid_pairs = list(_yield_valid_lock_key_pairs(locks, keys))

    res = len(valid_pairs)
    print(res)


def _load_locks_and_keys():
    with open("25.in") as file:
        schematic_chunks = file.read().split("\n\n")

    locks = list()
    keys = list()
    for chunk in schematic_chunks:
        schematic = chunk.strip().split("\n")
        top_line = schematic[0]
        bottom_line = schematic[-1]
        value_rows = schematic[1:-1]

        heights = [col.count(_FILLED) for col in zip(*value_rows)]

        assert top_line[0] != bottom_line[0]
        if top_line[0] == _FILLED:
            locks.append(heights)
        else:
            keys.append(heights)

    return locks, keys


def _yield_valid_lock_key_pairs(all_locks, all_keys):
    for lock in all_locks:
        for key in all_keys:
            height_sums = [l + k for l, k in zip(lock, key)]
            if not any(height > 5 for height in height_sums):
                yield (lock, key)


if __name__ == "__main__":
    main()
