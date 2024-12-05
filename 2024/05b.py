from collections import defaultdict, deque


def main():
    file_lines = _load_lines("05.in")
    rules_lines, updates_lines = _split_list(file_lines, "")

    before_to_afters_lookup = _build_rules_lookup(
        line.split("|") for line in rules_lines
    )
    updates = [line.split(",") for line in updates_lines]

    fixed_updates = [
        _fixed_update(upd, before_to_afters_lookup)
        for upd in updates
        if not _update_is_valid(upd, before_to_afters_lookup)
    ]
    res = sum(int(upd[len(upd) // 2]) for upd in fixed_updates)

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


def _fixed_update(update_pages, before_to_afters_lookup):
    new_update = list()
    for page in update_pages:
        # insert this page just before the earliest page that should be after
        # this one.
        afters = before_to_afters_lookup.get(page, set())
        after_indexes = [i for i, p in enumerate(new_update) if p in afters]
        if after_indexes:
            insert_index = min(after_indexes)
            new_update.insert(insert_index, page)
        else:
            new_update.append(page)
    return new_update


if __name__ == "__main__":
    main()
