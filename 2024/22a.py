_PRUNE_DIVISOR = 16777216


def main():
    initial_secrets = _load_initial_secrets()

    final_secrets = [_secret_after(secret, 2000) for secret in initial_secrets]

    res = sum(final_secrets)
    print(res)


def _load_initial_secrets():
    with open("22.in") as file:
        return [int(x) for x in file.readlines()]


def _secret_after(secret, num_iterations):
    for _ in range(num_iterations):
        secret = _next_secret(secret)
    return secret


def _next_secret(initial_secret):
    step1 = _prune(_mix(initial_secret, initial_secret * 64))
    step2 = _prune(_mix(step1, step1 // 32))
    step3 = _prune(_mix(step2, step2 * 2048))
    return step3


def _mix(secret, val):
    return secret ^ val


def _prune(secret):
    return secret % _PRUNE_DIVISOR


if __name__ == "__main__":
    main()
