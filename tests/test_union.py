
import math
from gsnlib.geometry import CSG
from gsnlib.geometry import Node
from gsnlib.geometry import Vector


def test_subtract():
    subject_polygon = CSG.from_polygons([[[10, 10], [100, 10], [50, 140]]])
    clip_polygon = CSG.from_polygons([[[10, 100], [50, 10], [100, 100]]])
    subject_polygon.subtract(clip_polygon)
    polygons = subject_polygon.subtract(clip_polygon).to_polygons()

    assert polygons is not None


def test_union():
    poly_a = CSG.from_polygons([[
        [0, 0],
        [15, 0],
        [15, 15],
        [0, 15]
        ]])

    poly_b = CSG.from_polygons([[
        [30, 30],
        [10, 30],
        [10, 10],
        [30, 10]
        ]])

    union = poly_a.union(poly_b)
    polygons = union.to_polygons()

    assert polygons is not None
    assert len(polygons) == 1, polygons
    assert len(polygons[0]) == 11, len(polygons[0])


def test_manual_union():
    poly_a = CSG.from_polygons([[
        [0, 0],
        [15, 0],
        [15, 15],
        [0, 15]
        ]])

    poly_b = CSG.from_polygons([[
        [30, 30],
        [10, 30],
        [10, 10],
        [30, 10]
        ]])

    a = Node(poly_a.clone().segments)
    assert len(a.all_segments()) == 4

    b = Node(poly_b.clone().segments)
    assert len(a.all_segments()) == 4

    a.invert()
    assert len(a.all_segments()) == 4
    b.clip_to(a)
    assert len(b.all_segments()) == 5
    b.invert()
    assert len(b.all_segments()) == 5
    a.clip_to(b)
    a_all_segments = a.all_segments()
    assert len(a.all_segments()) == 5
    b.clip_to(a)
    b_all_segments = b.all_segments()
    assert len(b.all_segments()) == 5

    segs = b.all_segments()
    assert len(segs) == 5

    a.build(segs)
    a_all_segments = a.all_segments()
    assert len(a.all_segments()) == 10

    a.invert()
    a_all_segments = a.all_segments()
    assert len(a.all_segments()) == 10


def test_subtract_2():
    poly_a = CSG.from_polygons([[
        [0, 0],
        [15, 0],
        [15, 15],
        [0, 15]
        ]])

    poly_b = CSG.from_polygons([[
        [30, 30],
        [10, 30],
        [10, 10],
        [30, 10]
        ]])

    polygons = poly_a.subtract(poly_b).to_polygons()

    assert polygons is not None
    assert len(polygons) == 1, len(polygons)
    assert len(polygons[0]) == 8, len(polygons[0])


def test_intersect():
    poly_a = CSG.from_polygons([[
        [0, 0],
        [15, 0],
        [15, 15],
        [0, 15]
        ]])

    poly_b = CSG.from_polygons([[
        [30, 30],
        [10, 30],
        [10, 10],
        [30, 10]
        ]])

    polygons = poly_a.intersect(poly_b).to_polygons()

    assert polygons is not None
    assert len(polygons) == 1, len(polygons)
    assert len(polygons[0]) == 5, len(polygons[0])


def test_circle_union():
    stepcount = 30

    def pol2cart(angle: float, radius: float = 1.0) -> Vector:
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        return Vector(x, y)

    def delta(i: float, steps: int = 36) -> float:
        return (math.pi * 2 / steps) * i

    def csg_circle(position: Vector = Vector(0, 0), size: float = 100) -> CSG:
        polygons = [pol2cart(delta(i, stepcount), size) + position
                    for i in range(stepcount)]
        return CSG.from_polygons([polygons])

    circles = [
        (Vector(0.0, 0.0, 0.0), 30, False),
        (Vector(13, 20, 0.0), 17, False),
        (Vector(2, 33, 0.0), 4, False),
        (Vector(0, 33, 0.0), 3, False)
    ]

    circles = [
        (Vector(0.0, 0.0, 0.0), 30, False),
        (Vector(9.159937903903145, -28.501722699929672, 0.0),
         1.9358049315341745, False),
        (Vector(9.000231775034093, -27.141412518165417, 0.0),
         1.3679879000715582, False),
    ]

    output = csg_circle(circles[0][0], circles[0][1])

    assert len(output.to_polygons()) == 1
    point_count = len(output.to_polygons()[0])

    for c in circles[1:]:
        next = csg_circle(c[0], c[1])
        output = output.union(next)
        polygons = output.to_polygons()
        assert len(polygons) == 1

        new_point_count = len(polygons[0])
        assert new_point_count > point_count, c

        point_count = new_point_count
