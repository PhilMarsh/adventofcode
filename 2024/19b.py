import functools


def main():
    towels, patterns = _load_towels_and_patterns()

    pattern_num_combos = {p: _num_pattern_towel_combos(p, towels) for p in patterns}

    res = sum(num for num in pattern_num_combos.values())
    print(res)


def _load_towels_and_patterns():
    with open("19.in") as file:
        file_lines = file.readlines()

    towels = tuple(file_lines[0].strip().split(", "))
    patterns = [p.strip() for p in file_lines[2:]]
    return towels, patterns


@functools.cache
def _num_pattern_towel_combos(pattern, towels):
    if not pattern:
        return 1

    return sum(
        _num_pattern_towel_combos(pattern[len(tow) :], towels)
        for tow in towels
        if pattern.startswith(tow)
    )


if __name__ == "__main__":
    main()
