import math
from gsnlib.structures import CircularSorted
from typing import List
from . import Shape, Polygon, Vector, ray_segment_intersection, Line


def calc_next(cur: int, count: int) -> int:
    return (cur + 1) % count


def calc_prev(cur: int, count: int) -> int:
    return (count + (cur - 1)) % count


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
    diff = math.atan2(b.y, b.x) - math.atan2(a.y, a.x)

    return diff % (math.pi * 2)


def is_convex(point: Vector, left: Vector, right: Vector) -> bool:
    return tri_angle(point, left, right) < math.pi


def triangulate(input: Polygon) -> List[Polygon]:
    if len(input.points) == 3:
        # The polygon is just a single triangle, return it!
        return [input, ]

    # List containing the index to each point in the polygon
    point_index: List[int] = list(range(len(input.points)))

    # Index to all points that currently are ears
    ear_index = CircularSorted()

    # Points in an interior angle larger than PI
    reflex_index: List[int] = []

    # Points in an interior angle smaller than PI
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

        # Calculate internal angle of current point
        r = tri_angle(vertex_current, vertex_prev, vertex_next)

        if r > math.pi:
            reflex_index.append(pos)
            # If it is not convex, it can not be an ear
            continue

        # Current point is convex, add it to convex list.
        convex_index.append(pos)

        # Check that no other point lies inside triangle formed
        # by current point + previous and next point.
        # This should be done with reflex vertices, but that
        # list is not complete at this point.
        cur_poly = Polygon([vertex_current, vertex_next, vertex_prev])
        check_points = [
            i for i in point_index if i not in [pos,  pos_next, pos_prev]]
        ear_check: bool = check_ear(
            cur_poly, [input.points[p] for p in check_points])

        if ear_check:
            # Current point is part of ear.
            ear_index.append(pos)

    # Resulting polygons
    polygons: List[Polygon] = []

    """
    Do the actual clipping.
    Remove each ear, one at a time.
    """
    while len(ear_index) > 0 and len(point_index) > 3:
        ear: int = ear_index[0]
        ear_point = point_index.index(ear)

        ear_prev: int = point_index[calc_prev(ear_point, len(point_index))]
        ear_next: int = point_index[calc_next(ear_point, len(point_index))]

        # indicies_ear = (ear_prev, ear, ear_next)

        polygon: Polygon = Polygon([
            input.points[ear_prev],
            input.points[ear],
            input.points[ear_next]
        ])
        polygons.append(polygon)

        # BUG: There is some miff in calculating the indexes here!

        # Left indicies
        ear_prev_prev = point_index[calc_prev(ear_prev, len(point_index))]
        ear_prev_next = point_index[calc_next(ear_point, len(point_index))]
        # indicies_left = [ear_prev, ear_prev_next, ear_prev_prev]
        left_r = tri_angle(
            input.points[ear_prev],
            input.points[ear_prev_prev],
            input.points[ear_prev_next])

        # Right indicies
        ear_next_prev = point_index[calc_prev(ear_point, len(point_index))]
        ear_next_next = point_index[calc_next(
            point_index.index(ear_next), len(point_index))]

        # These end up wrong at some point...

        # indicies_right = [ear_next, ear_next_prev, ear_next_next]
        right_r = tri_angle(
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
        if left_r > math.pi:
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

        if right_r > math.pi:
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
        # Only three points left, must be final triangle.
        polygon = Polygon([input.points[p] for p in point_index])
        polygons.append(polygon)

    return polygons


def collapse(shape: Shape) -> Polygon:
    ##
    # Assumptions
    # The first polygon is the main shape
    # All other polygons are of the opposite winding
    # All other polygons are completely inside the first

    # determine winding
    shell = shape.polygons[0]
    main_winding = shell.winding()

    for hole_poly in shape.polygons[1:]:
        assert hole_poly.winding() != main_winding

        # Find maximum x of inner poly
        max_point = None
        for idx, point in enumerate(hole_poly.points):
            if idx == 0:
                max_point = point
                continue

            if isinstance(max_point, Vector) and point.x > max_point.x:
                max_point = point

        if max_point is None:
            raise TypeError

        closest_intersection = None
        closest_segment = None
        print(f"Found max point in hole at {max_point}")
        for segment in shell.segments():
            intersection = ray_segment_intersection(
                Line(max_point, Vector(1, 0)), segment)

            if isinstance(intersection, Vector):
                print(
                    "Checking intersection of segment " +
                    f"{segment} at {intersection}")
                if isinstance(closest_intersection, Vector):
                    if ((intersection - max_point).length()
                            < (closest_intersection - max_point).length()):
                        closest_intersection = intersection
                        closest_segment = segment
                else:
                    closest_intersection = intersection
                    closest_segment = segment

        print(f"Closest intersection: {closest_intersection}")
        print(f"Closest segment: {closest_segment}")
        if closest_segment is not None:
            mutual_point = (closest_segment.start
                            if closest_segment.start.x > closest_segment.end.x
                            else closest_segment.end)

            print(mutual_point)

    return Polygon([])
