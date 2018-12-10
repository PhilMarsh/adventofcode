import sys
from collections import defaultdict

data = sys.stdin.read().strip().split("\n")

waiting = defaultdict(set)
done = list()
for line in data:
    print(line)
    dep, base = line.split(" must be finished before step ")
    dep = dep[-1]
    base = base[0]
    waiting[dep]
    waiting[base].add(dep)

while waiting:
    for k, v in sorted(waiting.items()):
        for dep in list(v):
            if dep not in waiting:
                v.remove(dep)
        if not v:
            done.append(k)
            del waiting[k]
            break

print("".join(done))
