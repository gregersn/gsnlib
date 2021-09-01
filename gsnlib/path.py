#!/usr/bin/env python
# -*- coding: utf8 -*-

import math
from typing import List
from .vector import Vector
from gsnlib.constants import EPSILON


def pointlinedist(p: Vector, p1: Vector, p2: Vector):
    dy = p2.y - p1.y
    dx = p2.x - p1.x

    a = abs(dy * p.x - dx * p.y + p2.x * p1.y - p2.y * p1.x)
    b = math.sqrt(dy * dy + dx * dx)

    if b < EPSILON:
        return p.dist(p1)
    return a / b


def reduce_shapes(shapes: List[List[List[Vector]]], tolerance: float):
    out = [[reduce_points(part, tolerance) for part in shape]
           for shape in shapes]
    return out


def reduce_points(points: List[Vector], tolerance: float) -> List[Vector]:
    dmax = 0
    index = 0
    end = len(points) - 1

    p0 = points[0]
    p1 = points[end]

    for i in range(1, end):
        d = pointlinedist(points[i], p0, p1)
        if d > dmax:
            dmax = d
            index = i

    if dmax > tolerance:
        res1 = reduce_points(points[0:index + 1], tolerance)
        res2 = reduce_points(points[index:], tolerance)
        outpoints = res1 + res2[1:]
    else:
        outpoints = [p0, p1]

    return outpoints


def main():
    pass


if __name__ == '__main__':
    main()
