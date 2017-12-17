import sys

def spinlock(step, end):
    buff = [0]
    pos = 0
    for i in range(1, end+1):
        pos = ((pos + step + 1) % i)
        buff.insert(pos, i)
    return buff

step = int(sys.argv[1])
buff = spinlock(step, 2017)
(last_pos,) = (i for i, val in enumerate(buff) if val == 2017)
print(buff[(last_pos+1) % len(buff)])