def main():
    stones = _load_stones()

    for _ in range(25):
        stones = _yield_blink_stones(stones)

    res = len(list(stones))
    print(res)


def _load_stones():
    with open("11.in") as file:
        return [int(x) for x in file.read().strip().split()]


def _yield_blink_stones(stones):
    for val in stones:
        if val == 0:
            yield 1
        elif (num_digits := len(str(val))) % 2 == 0:
            pow_10_mask = 10 ** (num_digits // 2)
            yield val // pow_10_mask
            yield val % pow_10_mask
        else:
            yield val * 2024


if __name__ == "__main__":
    main()
