import dataclasses


@dataclasses.dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __sub__(self, other):
        return __class__(x=self.x - other.x, y=self.y - other.y)

    def __add__(self, other):
        return __class__(x=self.x + other.x, y=self.y + other.y)

    def __mul__(self, scalar):
        return __class__(x=self.x * scalar, y=self.y * scalar)

    def __rmul__(self, scalar):
        """scalar multiplication is commutative."""
        return self * scalar

    def __truediv__(self, scalar):
        return __class__(x=self.x / scalar, y=self.y / scalar)

    def magnitude(self):
        return (self.x**2 + self.y**2) ** 0.5

    def unit(self):
        return self / self.magnitude()


@dataclasses.dataclass(frozen=True)
class Box:
    v1: Vector
    v2: Vector

    def __contains__(self, vector):
        return (
            self.v1.y <= vector.y <= self.v2.y or self.v1.y >= vector.y >= self.v2.y
        ) and (self.v1.x <= vector.x <= self.v2.x or self.v1.x >= vector.x >= self.v2.x)
