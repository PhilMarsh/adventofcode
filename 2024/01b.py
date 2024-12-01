from collections import defaultdict

def main():
    left = list()
    right = list()
    with open("./01.in") as file:
        for line in file:
            left_str, right_str = line.split()
            left.append(int(left_str))
            right.append(int(right_str))

    right_counts = defaultdict(int)
    for num in right:
        right_counts[num] += 1

    res = sum(
        a * right_counts.get(a, 0)
        for a in left
    )
    print(res)


if __name__ == "__main__":
    main()
