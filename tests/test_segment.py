from gsnlib.geometry import Segment, Vector


def test_repr():
    vertices = [
        Vector(0.0, 0.0),
        Vector(0.0, 10.0)
    ]
    segment = Segment(vertices=vertices)

    assert repr(
        segment) == "<Segment (Vector(0.0, 0.0, 0.0), Vector(0.0, 10.0, 0.0))>", repr(segment)


def test_new_segment():
    vertices = [
        Vector(0, 0),
        Vector(0, 10)
    ]
    segment = Segment(vertices=vertices)

    assert segment is not None
    assert segment.line.origin == Vector(0, 0)
    assert segment.line.direction == Vector(0, 1)
    assert segment.line.normal == Vector(1, 0)


def test_segment_flip():
    segment = Segment([
        Vector(0, 0),
        Vector(0, 10)
    ])

    assert segment.line.origin == Vector(0, 0)
    assert segment.line.direction == Vector(0, 1)
    assert segment.line.normal == Vector(1, 0)

    segment.flip()

    assert segment.vertices[1] == (Vector(0, 0))
    assert segment.vertices[0] == (Vector(0, 10))
    assert segment.line.origin == Vector(0, 0).negated()
    assert segment.line.direction == Vector(0, 1).negated()
    assert segment.line.normal == Vector(1, 0).negated()


def test_segment_copy():
    s1 = Segment([
        Vector(0, 0),
        Vector(0, 10)
    ])

    s2 = s1.clone()

    assert s1 == s2
    assert s1 is not s2
