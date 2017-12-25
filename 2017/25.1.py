from collections import defaultdict
import enum
import sys

class State(enum.Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"

class TM(object):
    def __init__(self):
        self.tape = defaultdict(bool)
        self.cursor_index = 0
        self.state = State.A

    @property
    def value(self):
        return self.tape[self.cursor_index]

    @value.setter
    def value(self, bit):
        self.tape[self.cursor_index] = bit

    def right(self):
        self.cursor_index += 1

    def left(self):
        self.cursor_index -= 1

    def state_a(self):
        if not self.value:
            self.value = True
            self.right()
            self.state = State.B
        else:
            self.value = False
            self.left()
            self.state = State.C

    def state_b(self):
        if not self.value:
            self.value = True
            self.left()
            self.state = State.A
        else:
            self.value = True
            self.left()
            self.state = State.D

    def state_c(self):
        if not self.value:
            self.value = True
            self.right()
            self.state = State.D
        else:
            self.value = False
            self.right()
            self.state = State.C

    def state_d(self):
        if not self.value:
            self.value = False
            self.left()
            self.state = State.B
        else:
            self.value = False
            self.right()
            self.state = State.E

    def state_e(self):
        if not self.value:
            self.value = True
            self.right()
            self.state = State.C
        else:
            self.value = True
            self.left()
            self.state = State.F

    def state_f(self):
        if not self.value:
            self.value = True
            self.left()
            self.state = State.E
        else:
            self.value = True
            self.right()
            self.state = State.A

    STATE_ACTION_LOOKUP = {
        State.A: state_a,
        State.B: state_b,
        State.C: state_c,
        State.D: state_d,
        State.E: state_e,
        State.F: state_f,
    }

    def execute(self, init_state, stop_after):
        self.state = init_state
        for _ in range(stop_after):
            if _ % 10**5 == 0:
                print(_)
            self.STATE_ACTION_LOOKUP[self.state](self)

tm = TM()

tm.execute(State.A, 12172063)

print(sum(tm.tape.values()))