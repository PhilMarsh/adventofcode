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
            yield (x, y)

paths = [
    set(gen_points(w))
    for w in wires
]

intersections = set.intersection(*paths)
print(intersections)
print(min(abs(x) + abs(y) for x, y in intersections))
