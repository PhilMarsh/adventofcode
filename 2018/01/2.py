import sys
from itertools import cycle

seen = set()
f = 0
for i in cycle(int(i) for i in sys.stdin.read().split() if i):
    f += i
    if f in seen:
        print(f)
        break
    seen.add(f)
