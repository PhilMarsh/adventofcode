import importlib


def _concat_ints(left, right):
    return int(str(left) + str(right))


if __name__ == "__main__":
    a = importlib.import_module("07a")
    a._OPERATORS += (_concat_ints,)
    a.main()
