import sys
print(sum(int(i) for i in sys.stdin.read().split() if i))
