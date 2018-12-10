import sys
from collections import defaultdict

data = sys.stdin.read().strip()

shortest = len(data)
for a, b in zip("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    old_data = None
    new_data = data.replace(a, "").replace(b, "")
    while old_data != new_data:
        old_data = new_data
        for x, y in zip("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            new_data = new_data.replace(x+y, "")
            new_data = new_data.replace(y+x, "")

    shortest = min(shortest, len(new_data))
    
print(shortest)
