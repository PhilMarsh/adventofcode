import sys
from collections import defaultdict
from copy import deepcopy

data = sys.stdin.read().strip().split("\n")

waiting = defaultdict(set)
ready = list()
for line in data:
    print(line)
    dep, base = line.split(" must be finished before step ")
    dep = dep[-1]
    base = base[0]
    waiting[dep]
    waiting[base].add(dep)

workers = [None]*5
time = 0
for k, v in sorted(waiting.items()):
    if not v:
        ready.append(k)
        del waiting[k]
while any(workers) or ready or waiting:
    print(time, workers)
    for i, w in enumerate(workers):
        if w:
            job, remaining = w
            if remaining == 1:
                workers[i] = None
                for k, v in sorted(waiting.items()):
                    v.discard(job)
                    if not v:
                        ready.append(k)
                        del waiting[k]
            else:
                workers[i] = (job, remaining-1)
        if not workers[i] and ready:
            job, ready = ready[0], ready[1:]
            workers[i] = (job, 61 + (ord(job) - ord("A")))
    time += 1

print(time-1)
