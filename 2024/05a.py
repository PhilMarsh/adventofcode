from collections import defaultdict


def main():
    file_lines = _load_lines("05.in")
    rules_lines, updates_lines = _split_list(file_lines, "")

    before_to_afters_lookup = _build_rules_lookup(
        line.split("|") for line in rules_lines
    )
    updates = [line.split(",") for line in updates_lines]

    res = sum(
        int(upd[len(upd) // 2])
        for upd in updates
        if _update_is_valid(upd, before_to_afters_lookup)
    )

    print(res)


def _load_lines(filename):
    with open(filename) as file:
        return [s.strip() for s in file.readlines()]


def _split_list(lst, delim):
    index = lst.index(delim)
    return lst[:index], lst[index + 1 :]


def _build_rules_lookup(rule_pairs):
    lookup = defaultdict(set)
    for before, after in rule_pairs:
        lookup[before].add(after)
    return dict(lookup)


def _update_is_valid(update_pages, before_to_afters_lookup):
    seen = set()
    for page in update_pages:
        afters = before_to_afters_lookup.get(page, set())
        if seen.intersection(afters):
            return False
        else:
            seen.add(page)
    return True


if __name__ == "__main__":
    main()
