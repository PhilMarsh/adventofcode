import sys

class Vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

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

    @property
    def dist(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

class Particle(object):
    def __init__(self, id_, p, v, a):
        self.id_ = id_
        self.p = p
        self.v = v
        self.a = a

    def __hash__(self):
        return hash(self.p)

    def __str__(self):
        return "<{0}, p={1}, v={2}, a={3}>".format(self.id_, self.p, self.v, self.a)

    def __eq__(self, rhs):
        return self.p == rhs.p #and self.v == rhs.v and self.a == rhs.a

    def __ne__(self, rhs):
        return not (self == rhs)

    def next(self):
        return Particle(
            self.id_,
            self.p + self.v + self.a,
            self.v + self.a,
            self.a
        )

particles = set()
destroyed = set()
for id_, line in enumerate(sys.stdin.readlines()):
    p = Particle(
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
    if p in particles:
        particles.remove(p)
        destroyed.add(p)
    elif p not in destroyed:
        particles.add(p)

# not exactly the most elegant, but seems like 10,000 iterations was enough.
# for true certainty, should probably be solving for quadratic equations
# being equal or something.
for _ in range(10**6):
    if _ % 10**4 == 0:
        print(_, len(particles))
    new_particles = set()
    destroyed = set()
    for p in particles:
        p = p.next()
        if p in new_particles:
            new_particles.remove(p)
            destroyed.add(p)
        elif p not in destroyed:
            new_particles.add(p)
    particles = new_particles
    if len(particles) < 2:
        break

print("len: {0}".format(len(particles)))