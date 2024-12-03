import re


_MUL_REGEX = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")


def main():
    data = _load_file("03.in")
    res = sum(int(a) * int(b) for a, b in _MUL_REGEX.findall(data))
    print(res)


def _load_file(filename):
    with open(filename) as file:
        return file.read()


if __name__ == "__main__":
    main()
