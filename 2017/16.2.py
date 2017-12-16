import collections
import sys

class Line(object):
    def __init__(self):
        self._state = "abcdefghijklmnop"

    def execute(self, moves):
        for action, args in moves:
            self.ACTION_LOOKUP_[action](self, *args)

    @property
    def state(self):
        return self._state

    def spin(self, n):
        self._state = self._state[-n:] + self._state[:-n]

    def exchange(self, a, b):
        self.partner(self._state[a], self._state[b])

    def partner(self, a, b):
        self._state = self._state.replace(a, "X").replace(b, a).replace("X", b)

    ACTION_LOOKUP_ = {
        "s": spin,
        "x": exchange,
        "p": partner
    }

def parse_move(s):
    s = s.strip()
    action = s[0]
    args = s[1:].split("/")
    if action in ("s", "x"):
        args = tuple(int(i) for i in args)
    return action, args

moves = tuple(
    parse_move(m)
    for m in sys.stdin.read().strip().split(",")
)

line = Line()
seen_states = collections.OrderedDict()
RUNS = 10**9
for i in range(RUNS):
    line.execute(moves)
    if line.state in seen_states:
        loop_start = seen_states[line.state]
        loop_size = i+1 - seen_states[line.state]
        final_loop_offset = (RUNS - loop_start) % loop_size
        for j in range(final_loop_offset):
            line.execute(moves)
        break
    seen_states[line.state] = i+1


print(line.state)