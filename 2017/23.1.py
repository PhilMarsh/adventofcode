from collections import namedtuple
import sys

Instruction = namedtuple(
    "Instruction",
    [
        "action",
        "args"
    ]
)

NOOP = Instruction("noop", tuple())

class Core(object):
    def __init__(self):
        self.registers = {
            c: 0
            for c in "abcdefgh"
        }
        self.mem = dict()
        self.progcount = 0

        self.mul_count = 0

    def load(self, start, data):
        self.mem.update(
            (start+i, d)
            for i, d in enumerate(data)
        )

    def execute(self, max_duration=float("inf")):
        try:
            duration = 0
            while (min(self.mem) <= self.progcount <= max(self.mem)
                    and duration < max_duration):
                inst = self.mem.get(self.progcount, NOOP)
                # print(inst)
                self._INSTRUCTION_LOOKUP[inst.action](self, *inst.args)
                self.progcount += 1
                duration += 1
        except:
            self._log("Uncaught Exception")
            raise
        if not (min(self.mem) <= self.progcount <= max(self.mem)):
            self._log(
                "Left program boundaries ({0}, {1}): {2}"
                .format(min(self.mem), max(self.mem), self.progcount)
            )
        else:
            self._log(
                "Reached Max Duration ({0}): {1}"
                .format(max_duration, duration)
            )

    def _resolve(self, val):
        if val.isalpha():
            return self.registers[val]
        return int(val)

    def _log(self, s):
        print(s)

    def _set(self, reg, val):
        self.registers[reg] = self._resolve(val)

    def _sub(self, reg, val):
        self.registers[reg] -= self._resolve(val)

    def _mul(self, reg, val):
        self.registers[reg] *= self._resolve(val)
        self.mul_count += 1

    def _jnz(self, cond, offset):
        if self._resolve(cond) != 0:
            self.progcount += self._resolve(offset)-1

    def _noop(self):
        pass

    _INSTRUCTION_LOOKUP = {
        "set": _set,
        "sub": _sub,
        "mul": _mul,
        "jnz": _jnz,
        "noop": _noop
    }

instructions = [
    Instruction(line[:3], line[4:].split())
    for line in sys.stdin.readlines()
]

p0 = Core()

p0.load(0, instructions)

p0.execute()

print(p0.mul_count)