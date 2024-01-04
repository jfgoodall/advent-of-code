from __future__ import annotations

from collections.abc import Iterable, Sequence
from numbers import Number


class Point2D(Sequence):
    __slots__ = ('x', 'y')

    def __init__(self, xy: Iterable[Number]=(0, 0)):
        self.x: Number
        self.y: Number
        self.x, self.y = xy

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return (self.x, self.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self):
        return 2

    def __getitem__(self, index: int) -> Number:
        return (self.x, self.y)[index]

    def __eq__(self, other) -> bool:
        return (self.x, self.y) == tuple(other)

    def __add__(self, other) -> Point2D:
        return Point2D((self.x + other[0], self.y + other[1]))

    def __iadd__(self, other) -> Point2D:
        self.x += other[0]
        self.y += other[1]
        return self

    def __sub__(self, other) -> Point2D:
        return Point2D((self.x - other[0], self.y - other[1]))

    def __isub__(self, other) -> Point2D:
        self.x -= other.x
        self.y -= other.y
        return self


class Point3D:
    __slots__ = ('x', 'y', 'z')
