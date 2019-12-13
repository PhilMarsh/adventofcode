def fuel(mass):
    f = mass // 3 - 2
    if f <= 0:
        return 0
    return f + fuel(f)

with open("input") as f:
    print(sum(fuel(int(i.strip())) for i in f.readlines() if i.strip()))


