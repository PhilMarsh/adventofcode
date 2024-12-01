def main():
    left = list()
    right = list()
    with open("./01.in") as file:
        for line in file:
            left_str, right_str = line.split()
            left.append(int(left_str))
            right.append(int(right_str))

    res = sum(
        abs(a - b)
        for a, b in zip(
            sorted(left),
            sorted(right),
        )
    )
    print(res)


if __name__ == "__main__":
    main()
