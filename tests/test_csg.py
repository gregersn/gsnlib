
import math
from gsnlib.geometry import CSG
from gsnlib.geometry import Vector


def test_from_polygons():
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

    polygons_a = poly_a.to_polygons()
    polygons_b = poly_b.to_polygons()

    assert len(polygons_a) == 1
    assert len(polygons_b) == 1

    assert len(polygons_a[0]) == 5
    assert len(polygons_b[0]) == 5

    assert polygons_a[0][0] == polygons_a[0][-1]
    assert polygons_b[0][0] == polygons_b[0][-1]
