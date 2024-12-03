import re


_INSTRUCTION_REGEX = re.compile(
    r"(?P<mul>mul)\((?P<a>\d{1,3}),(?P<b>\d{1,3})\)"
    r"|(?P<do>do)\(\)"
    r"|(?P<dont>don't)\(\)"
)


def main():
    data = _load_file("03.in")

    mul_enabled = True
    res = 0
    for match in _INSTRUCTION_REGEX.finditer(data):
        if match.group("mul") is not None:
            if mul_enabled:
                res += int(match.group("a")) * int(match.group("b"))
        elif match.group("do") is not None:
            mul_enabled = True
        elif match.group("dont") is not None:
            mul_enabled = False
        else:
            raise Exception(f"Unknown match: {match}")

    print(res)


def _load_file(filename):
    with open(filename) as file:
        return file.read()


if __name__ == "__main__":
    main()
