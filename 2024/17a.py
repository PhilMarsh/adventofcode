def main():
    program = _load_program()

    program.run()

    print(program.formatted_output())


def _load_program():
    with open("17.in") as file:
        file_lines = file.readlines()

    return Program(
        register_a=_parse_register_line(file_lines[0]),
        register_b=_parse_register_line(file_lines[1]),
        register_c=_parse_register_line(file_lines[2]),
        instructions=_parse_instructions_line(file_lines[4]),
    )


def _parse_register_line(line):
    return int(line.split(": ")[1])


def _parse_instructions_line(line):
    return line.split(": ")[1].strip().split(",")


class Program:
    def __init__(self, register_a, register_b, register_c, instructions):
        self._register_a = register_a
        self._register_b = register_b
        self._register_c = register_c
        self._instructions = tuple(instructions)

        self._instruction_index = 0
        self._output = list()

    def run(self):
        while not self._is_done():
            opcode = self._next_instruction()
            self._OPCODE_FUNCS[opcode](self)

    def formatted_output(self):
        return ",".join(self._output)

    def _is_done(self):
        return self._instruction_index >= len(self._instructions)

    def _next_instruction(self):
        next_inst = self._instructions[self._instruction_index]
        self._instruction_index += 1
        return next_inst

    def _next_literal_operand(self):
        return int(self._next_instruction())

    def _next_combo_operand(self):
        combo_operand = self._next_instruction()
        return self._COMBO_OPERAND_FUNCS[combo_operand](self)

    def _adv(self):
        self._register_a = self._register_a // (2 ** self._next_combo_operand())

    def _bdv(self):
        self._register_b = self._register_a // (2 ** self._next_combo_operand())

    def _cdv(self):
        self._register_c = self._register_a // (2 ** self._next_combo_operand())

    def _bxl(self):
        self._register_b = self._register_b ^ self._next_literal_operand()

    def _bxc(self):
        self._next_literal_operand()  # consume and ignore.
        self._register_b = self._register_b ^ self._register_c

    def _bst(self):
        self._register_b = self._next_combo_operand() % 8

    def _jnz(self):
        operand = self._next_literal_operand()  # consume even when no jump.
        if self._register_a != 0:
            self._instruction_index = operand

    def _out(self):
        self._output.append(str(self._next_combo_operand() % 8))

    _OPCODE_FUNCS = {
        "0": _adv,
        "1": _bxl,
        "2": _bst,
        "3": _jnz,
        "4": _bxc,
        "5": _out,
        "6": _bdv,
        "7": _cdv,
    }

    _COMBO_OPERAND_FUNCS = {
        "0": lambda self: 0,
        "1": lambda self: 1,
        "2": lambda self: 2,
        "3": lambda self: 3,
        "4": lambda self: self._register_a,
        "5": lambda self: self._register_b,
        "6": lambda self: self._register_c,
        # no 7.
    }


if __name__ == "__main__":
    main()
