input_range = range(145852, 616942)

def is_password(i):
    s = list(str(i))
    return s == sorted(s) and len(set(s)) < len(s)

passwords = [
    i
    for i in input_range
    if is_password(i)
]

print(passwords)
print(len(passwords))
