import sys

def spinlock(step, end, val_of_interest):
    pos = 0

    buff = [0]
    for i in range(1, val_of_interest+1):
        pos = ((pos + step + 1) % i)
        buff.insert(pos, i)
    pos_of_interest = pos
    next_value = buff[(pos+1) % len(buff)]

    for i in range(val_of_interest+1, end):
        if i % 10**6 == 0:
            print(i, pos, pos_of_interest, next_value)
        pos = ((pos + step + 1) % i)
        if pos == pos_of_interest:
            next_value = i
        elif pos < pos_of_interest:
            pos_of_interest += 1
    return next_value

step = int(sys.argv[1])
print(spinlock(step, 50*(10**6), val_of_interest=0))