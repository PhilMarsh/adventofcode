import sys
from collections import Counter

twos = set()
threes = set()
for box in sys.stdin.read().splitlines():
    if not box:
        continue
    c = Counter(box)
    if any(i == 2 for i in c.values()):
        twos.add(box)
    if any(i == 3 for i in c.values()):
        threes.add(box)

print(len(twos)*len(threes))
