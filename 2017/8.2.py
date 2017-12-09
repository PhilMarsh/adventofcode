import collections
import operator
import re
import sys

INST_REGEX = re.compile(
    r"(?P<dest_reg>\w+) (?P<dest_op>\w+) (?P<dest_val>\-?\d+)"
    r" if (?P<cond_reg>\w+) (?P<cond_op>[<>!=]+) (?P<cond_val>\-?\d+)"
)

Instruction = collections.namedtuple(
    "Instruction",
    [
        "dest_register",
        "dest_operator",
        "dest_value",
        "cond_register",
        "cond_operator",
        "cond_value"
    ]
)

DEST_OP_LOOKUP = {
    "inc": operator.add,
    "dec": operator.sub
}

COND_OP_LOOKUP = {
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne
}

def parse_instruction(line):
    m = INST_REGEX.match(line)
    return Instruction(
        dest_register=m.group("dest_reg"),
        dest_operator=DEST_OP_LOOKUP[m.group("dest_op")],
        dest_value=int(m.group("dest_val")),
        cond_register=m.group("cond_reg"),
        cond_operator=COND_OP_LOOKUP[m.group("cond_op")],
        cond_value=int(m.group("cond_val"))
    )

class ALU(object):
    def __init__(self):
        self.registers = collections.defaultdict(int)

    def execute(self, instructions):
        highest_value = None
        for inst in instructions:
            cond_register_value = self.registers[inst.cond_register]
            if inst.cond_operator(cond_register_value, inst.cond_value):
                dest_register_value = self.registers[inst.dest_register]
                dest_value = inst.dest_operator(
                    dest_register_value,
                    inst.dest_value
                )
                self.registers[inst.dest_register] = dest_value
                if highest_value is None or dest_value > highest_value:
                    highest_value = dest_value
        return highest_value

instructions = (
    parse_instruction(line)
    for line in sys.argv[1].splitlines()
)

alu = ALU()
print(alu.execute(instructions))
