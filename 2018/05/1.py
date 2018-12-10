import sys
from collections import defaultdict

data = sys.stdin.read().strip()

old_data = None
new_data = data
while old_data != new_data:
    old_data = new_data
    for x, y in zip("abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        new_data = new_data.replace(x+y, "")
        print(x+y, len(new_data))
        new_data = new_data.replace(y+x, "")
        print(y+x, len(new_data))
    print(len(new_data))

print(len(data))
print(len(new_data))
