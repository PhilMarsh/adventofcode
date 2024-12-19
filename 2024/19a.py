import functools


def main():
    towels, patterns = _load_towels_and_patterns()

    pattern_has_combos = {p: _has_pattern_towel_combo(p, towels) for p in patterns}

    res = sum(1 for has in pattern_has_combos.values() if has)
    print(res)


def _load_towels_and_patterns():
    with open("19.in") as file:
        file_lines = file.readlines()

    towels = tuple(file_lines[0].strip().split(", "))
    patterns = [p.strip() for p in file_lines[2:]]
    return towels, patterns


@functools.cache
def _has_pattern_towel_combo(pattern, towels):
    if not pattern:
        return True

    for tow in towels:
        if pattern.startswith(tow):
            if _has_pattern_towel_combo(pattern[len(tow) :], towels):
                return True

    return False


if __name__ == "__main__":
    main()
