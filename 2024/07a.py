import dataclasses
import itertools
import operator


_OPERATORS = (
    operator.add,
    operator.mul,
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
    operator_combos = itertools.product(_OPERATORS, repeat=len(spec.operands) - 1)
    return any(
        _apply_operators(op_combo, spec.operands) == spec.target
        for op_combo in operator_combos
    )


def _apply_operators(operators, operands):
    res = operands[0]
    for op, val in zip(operators, operands[1:]):
        res = op(res, val)
    return res


if __name__ == "__main__":
    main()
