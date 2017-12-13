import sys

def severity(depths_and_sizes, delay):
    severity = 0
    for depth, size in depths_and_sizes:
        cycle = (size *  2) - 2
        if (depth + delay) % cycle == 0:
            severity += (depth + 1) * size
    return severity

def yield_depth_and_size(lines):
    for l in lines:
        depth, size = l.split(": ")
        depth = int(depth)
        size = int(size)
        yield depth, size

def zero_severity_delay(depths_and_sizes):
    depths_and_sizes = list(depths_and_sizes)
    print(depths_and_sizes)
    for delay in range(9999999):
        sev = severity(depths_and_sizes, delay)
        # print(delay, sev)
        if sev == 0:
            return delay
    raise RuntimeError

print(zero_severity_delay(yield_depth_and_size(sys.stdin)))