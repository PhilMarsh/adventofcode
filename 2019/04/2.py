from collections import defaultdict

input_range = range(145852, 616942)

def is_password(i):
    s = list(str(i))
    if s != sorted(s):
        return False
    groups = defaultdict(int)
    for digit in s:
        groups[digit] += 1
    return 2 in groups.values()

passwords = [
    i
    for i in input_range
    if is_password(i)
]

print(passwords)
print(len(passwords))
