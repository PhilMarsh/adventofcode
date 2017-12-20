import sys

class Vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({0},{1},{2})".format(self.x, self.y, self.z)

    def __add__(self, rhs):
        return Vector(
            self.x + rhs.x,
            self.y + rhs.y,
            self.z + rhs.z
        )

    def __eq__(self, rhs):
        return self.dist == rhs.dist

    def __ne__(self, rhs):
        return not (self == rhs)

    def __lt__(self, rhs):
        return self.dist < rhs.dist

    def __gt__(self, rhs):
        return not (self == rhs or self < rhs)

    @property
    def dist(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

class Particle(object):
    def __init__(self, id_, p, v, a):
        self.id_ = id_
        self.p = p
        self.v = v
        self.a = a

    def __str__(self):
        return "<{0}, p={1}, v={2}, a={3}>".format(self.id_, self.p, self.v, self.a)

    def __eq__(self, rhs):
        return self.p == rhs.p and self.v == rhs.v and self.a == rhs.a

    def __ne__(self, rhs):
        return not (self == rhs)

    def __lt__(self, rhs):
        if self.a < rhs.a:
            return True
        if self.a > rhs.a:
            return False
        if self.v < rhs.v:
            return True
        if self.v > rhs.v:
            return False
        if self.p < rhs.p:
            return True
        if self.p > rhs.p:
            return False
        # all eq
        return False

    def __gt__(self, rhs):
        return not (self == rhs or self < rhs)

particles = [
    Particle(
        id_,
        *(
            Vector(
                *(
                    int(i)
                    for i in v.strip("<>pva=\n").split(",")
                )
            )
            for v in line.split(", ")
        )
    )
    for id_, line in enumerate(sys.stdin.readlines())
]

particles_by_closeness = sorted(particles)
print(
    [
        str(p)
        for p in particles_by_closeness[:10]
    ]
)