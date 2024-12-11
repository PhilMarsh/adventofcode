import functools


def main():
    stones = _load_stones()

    res = _num_stones_after_blinks(stones, num_blinks=75)

    print(res)


def _load_stones():
    with open("11.in") as file:
        return [int(x) for x in file.read().strip().split()]


def _num_stones_after_blinks(stones, *, num_blinks):
    return sum(
        _num_stones_after_blinks_of_single_stone(s, num_blinks=num_blinks)
        for s in stones
    )


@functools.cache
def _num_stones_after_blinks_of_single_stone(stone, *, num_blinks):
    if num_blinks == 0:
        return 1

    if stone == 0:
        next_stones = [1]
    elif (num_digits := len(str(stone))) % 2 == 0:
        pow_10_mask = 10 ** (num_digits // 2)
        next_stones = [
            stone // pow_10_mask,
            stone % pow_10_mask,
        ]
    else:
        next_stones = [stone * 2024]

    return _num_stones_after_blinks(next_stones, num_blinks=num_blinks - 1)


if __name__ == "__main__":
    main()
