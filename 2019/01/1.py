with open("input") as f:
    print(sum(int(i.strip()) // 3 - 2 for i in f.readlines() if i.strip()))
