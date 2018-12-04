import sys
from collections import Counter

ids = sys.stdin.read().strip().split()

for i in range(len(ids[0])):
    c = Counter(box[:i]+box[i+1:] for box in ids)
    matches = [box for box, count in c.items() if count == 2]
    if matches:
        print(matches[0])
        break
