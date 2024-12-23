from collections import defaultdict


_PRUNE_DIVISOR = 16777216


def main():
    initial_secrets = _load_initial_secrets()

    patterns_to_counts = _collect_patterns_to_counts(initial_secrets, 2000)

    largest_count, largest_pattern = max(
        (count, pattern) for pattern, count in patterns_to_counts.items()
    )

    print(largest_count, largest_pattern)


def _load_initial_secrets():
    with open("22.in") as file:
        return [int(x) for x in file.readlines()]


def _collect_patterns_to_counts(initial_secrets, num_iterations):
    all_patterns_to_counts = defaultdict(int)
    for secret in initial_secrets:
        seen_secret_patterns = set()
        for pattern, price in _yield_patterns_and_prices(secret, num_iterations):
            if pattern not in seen_secret_patterns:
                all_patterns_to_counts[pattern] += price
                seen_secret_patterns.add(pattern)
    return dict(all_patterns_to_counts)


def _yield_patterns_and_prices(initial_secret, num_iterations):
    secrets_iterators = (
        _iter_skip(_yield_secrets(initial_secret, num_iterations), skip)
        for skip in range(5)
    )
    for secrets_window in zip(*secrets_iterators):
        prices = [_price(secret) for secret in secrets_window]
        pattern = tuple(p2 - p1 for p1, p2 in zip(prices, prices[1:]))
        last_price = prices[-1]
        yield pattern, last_price


def _yield_secrets(secret, num_iterations):
    for _ in range(num_iterations):
        yield secret
        secret = _next_secret(secret)


def _next_secret(initial_secret):
    step1 = _prune(_mix(initial_secret, initial_secret * 64))
    step2 = _prune(_mix(step1, step1 // 32))
    step3 = _prune(_mix(step2, step2 * 2048))
    return step3


def _mix(secret, val):
    return secret ^ val


def _prune(secret):
    return secret % _PRUNE_DIVISOR


def _price(secret):
    return secret % 10


def _iter_skip(iterator, num):
    for _ in zip(range(num), iterator):
        pass
    return iterator


if __name__ == "__main__":
    main()
