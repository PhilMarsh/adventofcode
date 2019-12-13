with open("input") as f:
    base_program = [
        int(val)
        for val in f.read().split(",")
    ]

def _parse_opcode(val):
    s = str(val)
    return int(s[-2:]), tuple(int(digit) for digit in reversed(s[:-2]))

def _select_param(program, i, modes, offset):
    p = program[i + offset]
    modes_i = offset - 1
    if modes_i >= len(modes) or modes[modes_i] == 0:
        return program[p]
    elif modes[modes_i] == 1:
        return p
    else:
        raise Exception(f"bad mode: {modes[offset]}. param: {p}")

def _select_bin_op_params(program, i, modes):
    lhs = _select_param(program, i, modes, 1)
    rhs = _select_param(program, i, modes, 2)
    dest = program[i+3]
    return lhs, rhs, dest

class Add(object):
    CODE = 1
    
    @staticmethod
    def run(program, i, modes):
        lhs, rhs, dest = _select_bin_op_params(program, i, modes)
        program[dest] = lhs + rhs

        return i+4

class Mult(object):
    CODE = 2

    @staticmethod
    def run(program, i, modes):
        lhs, rhs, dest = _select_bin_op_params(program, i, modes)
        program[dest] = lhs * rhs

        return i+4

class Save(object):
    CODE = 3

    @staticmethod
    def run(program, i, modes):
        dest = program[i+1]
        program[dest] = int(input("? "))

        return i+2

class Dump(object):
    CODE = 4

    @staticmethod
    def run(program, i, modes):
        val = _select_param(program, i, modes, 1)
        print(val)

        return i+2

class JumpIfTrue(object):
    CODE = 5

    @staticmethod
    def run(program, i, modes):
        condition = _select_param(program, i, modes, 1)
        if condition:
            return _select_param(program, i, modes, 2)
        return i+3

class JumpIfFalse(object):
    CODE = 6

    @staticmethod
    def run(program, i, modes):
        condition = _select_param(program, i, modes, 1)
        if not condition:
            return _select_param(program, i, modes, 2)
        return i+3

class LessThan(object):
    CODE = 7

    @staticmethod
    def run(program, i, modes):
        lhs, rhs, dest = _select_bin_op_params(program, i, modes)
        program[dest] = int(lhs < rhs)

        return i+4

class Equals(object):
    CODE = 8

    @staticmethod
    def run(program, i, modes):
        lhs, rhs, dest = _select_bin_op_params(program, i, modes)
        program[dest] = int(lhs == rhs)

        return i+4

class Halt(object):
    CODE = 99
    
    @staticmethod
    def run(program, i, modes):
        print("done")
        raise SystemExit()

operations = {
    cls.CODE: cls
    for cls in (
        Add, Mult, Save, Dump, Halt,
        JumpIfTrue, JumpIfFalse, LessThan, Equals
    )
}

def run():
    program = list(base_program)

    i = 0
    while True:
        opcode, modes = _parse_opcode(program[i])
        op = operations[opcode]
        i = op.run(program, i, modes)

    return program[0]

run()
