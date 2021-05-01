import math
from typing import List, Union
from . import Shape, Polygon, Vector


def calc_next(cur: int, max: int) -> int:
    return (cur + 1) % max


def calc_prev(cur: int, max: int) -> int:
    return (max + (cur - 1)) % max


def check_ear(poly: Polygon, points: List[Vector]) -> bool:
    ear = True
    for point in points:
        if poly.contains(point):
            ear = False
            break

    return ear


def tri_angle(point: Vector, left: Vector, right: Vector) -> float:
    a = left - point
    b = right - point

    return (math.atan2(a.y, a.x) - math.atan2(b.y, b.x)) % (math.pi * 2)


def triangulate(input: Polygon) -> List[Polygon]:
    polygons: List[Polygon] = []
    if len(input.points) == 3:
        return [input, ]

    point_index: List[int] = list(range(len(input.points)))
    ear_index: List[int] = []
    reflex_index: List[int] = []
    convex_index: List[int] = []

    """
    Build initial lists of points and pointers and indexes.
    """
    for pos, _ in enumerate(input.points):
        vertex_current = input.points[pos]

        pos_next = calc_next(pos, len(input.points))
        pos_prev = calc_prev(pos, len(input.points))

        vertex_next = input.points[pos_next]
        vertex_prev = input.points[pos_prev]

        r = tri_angle(vertex_current, vertex_next, vertex_prev)

        if r > math.pi:
            reflex_index.append(pos)
            # If it is not convex, it can not be an ear
            continue

        convex_index.append(pos)

        cur_poly = Polygon([vertex_current, vertex_next, vertex_prev])
        check_points = [
            i for i in point_index if i not in [pos,  pos_next, pos_prev]]
        ear_check: bool = check_ear(
            cur_poly, [input.points[p] for p in check_points])

        if ear_check:
            ear_index.append(pos)

    """
    Do the actual clipping.
    """
    while len(ear_index) > 0 and len(point_index) > 3:
        ear_index = sorted(ear_index)
        # reflex = sorted(reflex)
        # convex = sorted(convex)
        ear: int = ear_index[0]
        ear_point = point_index.index(ear)

        ear_prev: int = point_index[(
            len(point_index) + (ear_point - 1)) % len(point_index)]
        ear_next: int = point_index[(ear_point + 1) % len(point_index)]

        indicies_ear = (ear_prev, ear, ear_next)

        polygon: Polygon = Polygon([
            input.points[ear_prev],
            input.points[ear],
            input.points[ear_next]
        ])
        polygons.append(polygon)

        # Left indicies
        ear_prev_prev = point_index[calc_prev(ear_prev, len(point_index))]
        ear_prev_next = point_index[calc_next(ear_prev, len(point_index))]
        indicies_left = [ear_prev, ear_prev_next, ear_prev_prev]
        r = tri_angle(
            input.points[ear_prev],
            input.points[ear_prev_next],
            input.points[ear_prev_prev])

        # Right indicies
        ear_next_prev = point_index[calc_prev(ear_next, len(point_index))]
        ear_next_next = point_index[calc_next(ear_next, len(point_index))]
        indicies_right = [ear_next, ear_next_prev, ear_next_next]
        r = tri_angle(
            input.points[ear_next],
            input.points[ear_next_prev],
            input.points[ear_next_next]
        )

        if ear in point_index:
            point_index.remove(ear)
        else:
            raise IndexError

        if ear in convex_index:
            convex_index.remove(ear)
        if ear in reflex_index:
            reflex_index.remove(ear)

        # Test to the left
        if r > math.pi:
            if ear_prev in ear_index:
                ear_index.remove(ear_prev)

            if ear_prev in convex_index:
                convex_index.remove(ear_prev)

            if ear_prev not in reflex_index:
                reflex_index.append(ear_prev)
        else:
            if ear_prev in reflex_index:
                reflex_index.remove(ear_prev)

            if ear_prev not in convex_index:
                convex_index.append(ear_prev)

            cur_poly = Polygon([input.points[ear_prev],
                                input.points[ear_prev_next],
                                input.points[ear_prev_prev]])
            check_points = [
                i for i in point_index if i not in [ear_prev, ear_prev_next,
                                                    ear_prev_prev]]
            ear_check = check_ear(cur_poly, [input.points[p]
                                             for p in check_points])

            if ear_check and ear_prev not in ear_index:
                ear_index.append(ear_prev)

        # Test to right

        if r > math.pi:
            if ear_next in ear_index:
                ear_index.remove(ear_next)

            if ear_next in convex_index:
                convex_index.remove(ear_next)

            if ear_next not in reflex_index:
                reflex_index.append(ear_next)
        else:
            if ear_next in reflex_index:
                reflex_index.remove(ear_next)

            if ear_next not in convex_index:
                convex_index.append(ear_next)

            # Check if ear
            cur_poly = Polygon([input.points[ear_next],
                                input.points[ear_next_next],
                                input.points[ear_next_prev]])
            check_points = [
                i for i in point_index if i not in [ear_next, ear_next_next,
                                                    ear_next_prev]]
            ear_check = check_ear(cur_poly, [input.points[p]
                                             for p in check_points])

            if ear_check and ear_next not in ear_index:
                ear_index.append(ear_next)

        ear_index.remove(ear)

    if len(point_index) == 3:
        polygon = Polygon([input.points[p] for p in point_index])
        polygons.append(polygon)

    return polygons
