import dataclasses
import itertools
import operator


_OPERATORS = (
    operator.add,
    operator.mul,
    lambda a, b: int(str(a) + str(b)),
)


@dataclasses.dataclass
class _EquationSpec:
    target: int
    operands: list[int]


def main():
    equation_specs = _yield_equation_specs()

    res = sum(spec.target for spec in equation_specs if _equation_is_valid(spec))

    print(res)


def _yield_equation_specs():
    with open("07.in") as file:
        for line in file:
            target, operands = line.strip().split(":")
            yield _EquationSpec(
                target=int(target), operands=[int(op) for op in operands.split()]
            )


def _equation_is_valid(spec):
    return any(
        _yield_operator_matches(
            target=spec.target, acc=spec.operands[0], operands=spec.operands[1:]
        )
    )


def _yield_operator_matches(*, target, acc, operands, operators_to_here=()):
    if not operands:
        if acc == target:
            yield operators_to_here
        return

    head, *rest = operands
    for op in _OPERATORS:
        next_acc = op(acc, head)
        if next_acc > target:
            # prune because we have prior knowledge that all operations increase
            # the result. there are no negative numbers, zeroes, or fractional
            # values to cause addition or multiplication to reduce the result.
            continue
        else:
            yield from _yield_operator_matches(
                target=target,
                acc=next_acc,
                operands=rest,
                operators_to_here=operators_to_here + (op,),
            )


if __name__ == "__main__":
    main()
