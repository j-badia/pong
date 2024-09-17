import math, numbers

def vector_from_polar(length, angle):
    v = Vector(0, 0)
    v.polar = length, angle
    return v

class Vector(object):
    def __init__(self, x_or_pair, y=None):
        if y is None:
            self.x, self.y = x_or_pair
        else:
            self.x = x_or_pair
            self.y = y

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid key {}".format(key))

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid key {}".format(key))

    def __repr__(self):
        return "Vector({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return len(self) != 0

    def __add__(self, other):
        if hasattr(other, "__getitem__"):
            if len(other) == 2:
                return Vector(self.x + other[0], self.y + other[1])
            else:
                return NotImplemented
        else:
            return Vector(self.x + other, self.y + other)

    __radd__ = __add__

    def __iadd__(self, other):
        if hasattr(other, "__getitem__"):
            if len(other) == 2:
                self.x += other[0]
                self.y += other[1]
            else:
                return NotImplemented
        else:
            self.x += other
            self.y += other
        return self

    def __sub__(self, other):
        if hasattr(other, "__getitem__"):
            if len(other) == 2:
                return Vector(self.x - other[0], self.y - other[1])
            else:
                return NotImplemented
        else:
            return Vector(self.x - other, self.y - other)

    def __rsub__(self, other):
        if hasattr(other, "__getitem__"):
            if len(other) == 2:
                return Vector(other[0] - self.x, other[1] - self.y)
            else:
                return NotImplemented
        else:
            return Vector(other - self.x, other - self.y)

    def __isub__(self, other):
        if hasattr(other, "__getitem__"):
            if len(other) == 2:
                self.x -= other[0]
                self.y -= other[1]
            else:
                return NotImplemented
        else:
            self.x -= other
            self.y -= other
        return self

    def __mul__(self, other):
        if not isinstance(other, numbers.Real):
            return NotImplemented
        return Vector(self.x*other, self.y*other)

    __rmul__ = __mul__

    def __imul__(self, other):
        if not isinstance(other, numbers.Real):
            return NotImplemented
        self.x *= other
        self.y *= other
        return self

    def __div__(self, other):
        if not isinstance(other, numbers.Real):
            return NotImplemented
        return Vector(self.x/other, self.y/other)

    def __idiv__(self, other):
        if not isinstance(other, numbers.Real):
            return NotImplemented
        self.x /= other
        self.y /= other
        return self

    def __truediv__(self, other):
        if not isinstance(other, numbers.Real):
            return NotImplemented
        return self.__div__(float(other))

    def __itruediv__(self, other):
        if not isinstance(other, numbers.Real):
            return NotImplemented
        return self.__idiv__(float(other))

    def __neg__(self):
        return Vector(-self.x, -self.y)

    @property
    def length(self):
        return math.hypot(self.x, self.y)

    @length.setter
    def length(self, value):
        self.polar = value, self.angle

    @property
    def polar(self):
        return (self.length, math.atan2(self.y, self.x))

    @polar.setter
    def polar(self, coords):
        self.x = coords[0] * math.cos(coords[1])
        self.y = coords[0] * math.sin(coords[1])

    def rotate(self, angle):
        self.polar = (self.length, self.polar[1]+angle)

    @property
    def angle(self):
        return self.polar[1]

    @angle.setter
    def angle(self, value):
        self.polar = self.length, value