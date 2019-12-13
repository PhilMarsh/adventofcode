with open("input") as f:
    wires = tuple( 
        tuple(
            (segment[0], int(segment[1:]))
            for segment in line.split(",")
        )
        for line in f.readlines()
    )

def gen_points(wire):
    x = 0
    y = 0
    total_dist = 0
    seen = set()
    for direction, distance in wire:
        dx = 0
        dy = 0
        if direction == "U":
            dy = 1
        elif direction == "D":
            dy = -1
        elif direction == "L":
            dx = -1
        else:
            dx = 1
        for _ in range(distance):
            x += dx
            y += dy
            total_dist += 1
            pos = (x, y)
            if pos not in seen:
                yield (pos, total_dist)
                seen.add(pos)

paths = [
    dict(gen_points(w))
    for w in wires
]

intersections = set.intersection(*(set(p.keys()) for p in paths))
print(intersections)
print(min(sum(p[pos] for p in paths) for pos in intersections))
