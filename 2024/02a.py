def main():
    res = sum(1 for report in _yield_reports("02.in") if _is_safe(report))
    print(res)


def _yield_reports(filename):
    with open(filename) as file:
        for line in file:
            yield [int(s) for s in line.split()]


def _is_safe(report):
    last = report[0]
    direction = None
    for val in report[1:]:
        diff = val - last
        diff_mag = abs(diff)
        if diff_mag < 1 or diff_mag > 3:
            return False

        if direction is None:
            direction = diff
        elif (diff < 0) != (direction < 0):
            return False

        last = val

    return True


if __name__ == "__main__":
    main()
