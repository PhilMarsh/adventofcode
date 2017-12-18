from collections import defaultdict, namedtuple
import queue
import sys
import threading
import time

Instruction = namedtuple(
    "Instruction",
    [
        "action",
        "args"
    ]
)

NOOP = Instruction("noop", tuple())

class Core(object):
    def __init__(self, pid, msgs_in, msgs_out, io_max_wait=5):
        self.pid = pid
        self.msgs_in = msgs_in
        self.msgs_out = msgs_out
        self.io_max_wait = io_max_wait

        self.registers = defaultdict(int)
        self.mem = dict()
        self.progcount = 0
        self.snd_count = 0
        self.rcv_count = 0

        self.registers["p"] = self.pid

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
        print("[{0}] {1}".format(self.pid, s))

    def _snd(self, val):
        self.snd_count += 1
        self._log("snd {0}: {1}".format(self.snd_count, self._resolve(val)))
        self.msgs_out.put(self._resolve(val), timeout=self.io_max_wait)
        self._log("snd'd {0}".format(self.snd_count))

    def _set(self, reg, val):
        self.registers[reg] = self._resolve(val)

    def _add(self, reg, val):
        self.registers[reg] += self._resolve(val)

    def _mul(self, reg, val):
        self.registers[reg] *= self._resolve(val)

    def _mod(self, reg, val):
        self.registers[reg] %= self._resolve(val)

    def _rcv(self, reg):
        self.rcv_count += 1
        self._log("rcv {0}: {1}".format(self.rcv_count, reg))
        self.registers[reg] = self.msgs_in.get(timeout=self.io_max_wait)
        self._log("rcv'd {0}: {1}".format(self.rcv_count, self.registers[reg]))

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

p0_msgs_in = queue.Queue()
p1_msgs_in = queue.Queue()

p0 = Core(0, p0_msgs_in, p1_msgs_in, io_max_wait=5)
p1 = Core(1, p1_msgs_in, p0_msgs_in, io_max_wait=5)

p0.load(0, instructions)
p1.load(0, instructions)

t0 = threading.Thread(
    target=p0.execute,
    # kwargs={"max_duration": 10000}
)
t1 = threading.Thread(
    target=p1.execute,
    # kwargs={"max_duration": 10000}
)

t1.start()
t0.start()

while any(t.is_alive() for t in (t0, t1)):
    time.sleep(1)

print("snd/rcv")
for p in (p0, p1):
    print("{0}: {1}/{2}".format(p.pid, p.snd_count, p.rcv_count))