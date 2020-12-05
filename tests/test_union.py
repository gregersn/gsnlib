from gsnlib.geometry import CSG


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

    polygons = poly_a.union(poly_b).to_polygons()

    assert polygons is not None
    assert len(polygons) == 1, polygons
    assert len(polygons[0]) == 11, len(polygons[0])


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
