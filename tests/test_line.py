from gsnlib.vector import Vector
from gsnlib.geometry import Line
from gsnlib.geometry import Segment


def test_from_points():
    line = Line.from_points(Vector(0, 0), Vector(0, 10))

    assert line.origin.x == 0
    assert line.origin.y == 0

    assert line.direction.x == 0
    assert line.direction.y == 1

    line = Line.from_points(Vector(0, 0), Vector(5, 0))

    assert line.origin.x == 0
    assert line.origin.y == 0

    assert line.direction.x == 1
    assert line.direction.y == 0


def test_clone():
    line = Line(Vector(0, 0), Vector(1, 0))
    line2 = line.clone()

    assert line is not line2


def test_flip():
    line = Line.from_points(Vector(0, 0), Vector(0, 10))

    assert line.origin.x == 0
    assert line.origin.y == 0

    assert line.direction.x == 0
    assert line.direction.y == 1

    line.flip()

    assert line.origin.x == 0
    assert line.origin.y == 0

    assert line.direction.x == 0
    assert line.direction.y == -1


def test_split_segment():
    s = Segment([Vector(-10, 0), Vector(10, 0)])

    line = Line.from_points(Vector(0, 0), Vector(0, 10))

    coright = []
    coleft = []
    right = []
    left = []
    line.split_segment(s, coright, coleft, right, left)

    assert not coright
    assert not coleft

    assert right
    assert left

    assert len(right) == 1
    assert len(left) == 1

    assert right[0].vertices[0].x == -10.0
    assert right[0].vertices[0].y == 0.0

    assert right[0].vertices[1].x == 0.0
    assert right[0].vertices[1].y == 0.0

    assert left[0].vertices[0].x == 0.0
    assert left[0].vertices[0].y == 0.0

    assert left[0].vertices[1].x == 10.0
    assert left[0].vertices[1].y == 0.0

    s = Segment([Vector(5, 0), Vector(10, 0)])

    line = Line.from_points(Vector(0, 0), Vector(0, 10))

    coright = []
    coleft = []
    right = []
    left = []
    line.split_segment(s, coright, coleft, right, left)

    assert not coright
    assert not coleft

    assert not right
    assert left

    assert len(right) == 0
    assert len(left) == 1


def test_split_segment_2():
    segments = [
        Segment([Vector(0, 0), Vector(0, 10)]),
        Segment([Vector(0, 10), Vector(10, 10)]),
        Segment([Vector(10, 10), Vector(0, 0)])
    ]

    line = segments[0].line.clone()

    right = []
    left = []
    seg = []

    for segment in segments:
        line.split_segment(segment, seg, seg, right, left)

    assert len(seg) == 1, seg
    assert len(right) == 0, right
    assert len(left) == 2, left


def test_split_segment_3():
    segments = [
        Segment([Vector(0, 10), Vector(10, 10)]),
        Segment([Vector(10, 10), Vector(0, 0)])
    ]

    line = segments[0].line.clone()

    right = []
    left = []
    seg = []

    for segment in segments:
        line.split_segment(segment, seg, seg, right, left)

    assert len(seg) == 1, seg
    assert len(right) == 0, right
    assert len(left) == 1, left


def test_split_segment_4():
    segments = [
        Segment([Vector(10, 10), Vector(0, 0)])
    ]

    line = segments[0].line.clone()

    right = []
    left = []
    seg = []

    for segment in segments:
        line.split_segment(segment, seg, seg, right, left)

    assert len(seg) == 1, seg
    assert len(right) == 0, right
    assert len(left) == 0, left


def test_split_segments():
    right = []
    left = []
    seg = []

    segments = [
        Segment([Vector(0, 0), Vector(0, 10)]),
        Segment([Vector(0, 10), Vector(10, 10)]),
        Segment([Vector(10, 10), Vector(0, 0)]),
    ]

    line = segments[0].line.clone()

    for segment in segments:
        line.split_segment(segment,
                           seg,
                           seg,
                           right,
                           left)
