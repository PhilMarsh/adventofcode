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
    min: Vector
    max: Vector

    def __init__(self, v1, v2):
        # need to call `object.__setattr__()` to work around `frozen=True`
        # during setup.
        object.__setattr__(self, "min", Vector(x=min(v1.x, v2.x), y=min(v1.y, v2.y)))
        object.__setattr__(self, "max", Vector(x=max(v1.x, v2.x), y=max(v1.y, v2.y)))

    def __contains__(self, vector):
        return (self.min.y <= vector.y <= self.max.y) and (
            self.min.x <= vector.x <= self.max.x
        )
