from collections import defaultdict, namedtuple
import sys

Instruction = namedtuple(
    "Instruction",
    [
        "action",
        "args"
    ]
)

NOOP = Instruction("noop", tuple())

class ALU(object):
    def __init__(self):
        self.registers = defaultdict(int)
        self.mem = dict()
        self.progcount = 0
        self.last_sound = None

    def load(self, start, data):
        self.mem.update(
            (start+i, d)
            for i, d in enumerate(data)
        )

    def execute(self, max_duration=float("inf")):
        duration = 0
        while (min(self.mem) <= self.progcount <= max(self.mem)
                and duration < max_duration):
            inst = self.mem.get(self.progcount, NOOP)
            # print(inst)
            self._INSTRUCTION_LOOKUP[inst.action](self, *inst.args)
            self.progcount += 1
            duration += 1

    def _resolve(self, val):
        if val.isalpha():
            return self.registers[val]
        return int(val)

    def _snd(self, freq):
        self.last_sound = self._resolve(freq)
        print("snd: {0}".format(self.last_sound))

    def _set(self, reg, val):
        self.registers[reg] = self._resolve(val)

    def _add(self, reg, val):
        self.registers[reg] += self._resolve(val)

    def _mul(self, reg, val):
        self.registers[reg] *= self._resolve(val)

    def _mod(self, reg, val):
        self.registers[reg] %= self._resolve(val)

    def _rcv(self, cond):
        if self._resolve(cond) != 0:
            print("rcv: {0}".format(self.last_sound))

    def _jgz(self, cond, offset):
        if self._resolve(cond) > 0:
            self.progcount += self._resolve(offset)-1

    def _noop(self):
        pass

    _INSTRUCTION_LOOKUP = {
        "snd": _snd,
        "set": _set,
        "add": _add,
        "mul": _mul,
        "mod": _mod,
        "rcv": _rcv,
        "jgz": _jgz,
        "noop": _noop
    }

instructions = [
    Instruction(line[:3], line[4:].split())
    for line in sys.stdin.readlines()
]

alu = ALU()

alu.load(0, instructions)

alu.execute(2000)