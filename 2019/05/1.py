with open("input") as f:
    base_program = [
        int(val)
        for val in f.read().split(",")
    ]

def _parse_opcode(val):
    s = str(val)
    return int(s[-2:]), tuple(int(digit) for digit in reversed(s[:-2]))

def _select_one_param(program, params, modes, i):
    p = params[i]
    if i >= len(modes) or modes[i] == 0:
        return program[p]
    elif modes[i] == 1:
        return p
    else:
        raise Exception(f"bad mode: {modes[i]}. param: {p}")

class Add(object):
    CODE = 1
    SIZE = 4
    
    @staticmethod
    def run(program, params, modes):
        lhs = _select_one_param(program, params, modes, 0)
        rhs = _select_one_param(program, params, modes, 1)
        dest = params[2]
        program[dest] = lhs + rhs

class Mult(object):
    CODE = 2
    SIZE = 4

    @staticmethod
    def run(program, params, modes):
        lhs = _select_one_param(program, params, modes, 0)
        rhs = _select_one_param(program, params, modes, 1)
        dest = params[2]
        program[dest] = lhs * rhs

class Save(object):
    CODE = 3
    SIZE = 2

    @staticmethod
    def run(program, params, modes):
        dest = params[0]
        program[dest] = int(input("? "))

class Dump(object):
    CODE = 4
    SIZE = 2

    @staticmethod
    def run(program, params, modes):
        val = _select_one_param(program, params, modes, 0)
        print(val)

class Halt(object):
    CODE = 99
    SIZE = 1
    
    @staticmethod
    def run(program, params, modes):
        print("done")
        raise SystemExit()

operations = {
    cls.CODE: cls
    for cls in (Add, Mult, Save, Dump, Halt)
}

def run():
    program = list(base_program)

    i = 0
    while True:
        opcode, modes = _parse_opcode(program[i])
        op = operations[opcode]
        params = program[i+1:i+op.SIZE]
        op.run(program, params, modes)
        i += op.SIZE

    return program[0]

run()
