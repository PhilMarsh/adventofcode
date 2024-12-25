from collections import defaultdict, deque
import dataclasses
from enum import Enum
import operator
import re


_INITIAL_WIRE_VALUE_REGEX = re.compile(r"(?P<wire>\w+): (?P<value>[01])")
_GATE_REGEX = re.compile(
    r"(?P<left_wire>\w+) (?P<operator>(AND|OR|XOR)) (?P<right_wire>\w+) -> (?P<out_wire>\w+)"
)


def main():
    initial_wire_values, gates = _load_input()

    final_wire_values = _propogate(gates, initial_wire_values)

    res = _extract_z_output(final_wire_values)
    print(res)


class _Operator(Enum):
    AND = "AND"
    OR = "OR"
    XOR = "XOR"


_OPERATOR_FUNCS = {
    _Operator.AND: operator.and_,
    _Operator.OR: operator.or_,
    _Operator.XOR: operator.xor,
}


@dataclasses.dataclass(frozen=True)
class _Gate:
    in_wires: tuple[str, str]
    out_wire: str
    operator: _Operator


def _load_input():
    with open("24.in") as file:
        initial_wire_value_lines, gate_lines = file.read().split("\n\n")

    initial_wire_values = {
        m.group("wire"): int(m.group("value"))
        for line in initial_wire_value_lines.split("\n")
        if (m := _INITIAL_WIRE_VALUE_REGEX.match(line.strip()))
    }

    gates = [
        _Gate(
            in_wires=(m.group("left_wire"), m.group("right_wire")),
            operator=_Operator(m.group("operator")),
            out_wire=m.group("out_wire"),
        )
        for line in gate_lines.split("\n")
        if (m := _GATE_REGEX.match(line.strip()))
    ]

    return initial_wire_values, gates


def _propogate(gates, initial_wire_values):
    final_wire_values = dict(initial_wire_values)

    wires_newly_ready = deque(initial_wire_values.keys())

    wires_to_gates_waiting = defaultdict(list)
    for gat in gates:
        for wire in gat.in_wires:
            wires_to_gates_waiting[wire].append(gat)

    while wires_to_gates_waiting:
        ready_wire = wires_newly_ready.popleft()
        gates = wires_to_gates_waiting.pop(ready_wire, tuple())
        for gat in gates:
            if gat.out_wire in final_wire_values:
                # already processed by the other in-wire.
                continue

            try:
                in_values = [final_wire_values[iw] for iw in gat.in_wires]
            except KeyError:
                # not all wires are ready yet.
                continue

            op_func = _OPERATOR_FUNCS[gat.operator]
            final_wire_values[gat.out_wire] = op_func(*in_values)
            wires_newly_ready.append(gat.out_wire)

    return final_wire_values


def _extract_z_output(wire_values):
    exp_values = {
        int(wire[1:]): val for wire, val in wire_values.items() if wire.startswith("z")
    }
    return sum(2**exp * val for exp, val in exp_values.items())


if __name__ == "__main__":
    main()
