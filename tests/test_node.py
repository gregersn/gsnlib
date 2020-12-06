from gsnlib.geometry import Node, Segment, Vector


def test_init_node():
    segments = [
        Segment([Vector(0, 0), Vector(0, 10)]),
        Segment([Vector(0, 10), Vector(10, 10)]),
        Segment([Vector(10, 10), Vector(0, 0)])
    ]
    n = Node(segments)

    assert n is not None

    assert len(n.segments) == 1
    assert n.line == Segment([Vector(0, 0), Vector(0, 10)]).line
    assert not n.right
    assert n.left


def test_node_invert():
    segments = [
        Segment([Vector(0, 0), Vector(0, 10)]),
        Segment([Vector(0, 10), Vector(10, 10)]),
        Segment([Vector(10, 10), Vector(0, 0)])
    ]
    n = Node(segments)
    n.invert()

    assert n is not None

    assert len(n.segments) == 1
    assert n.line == Segment([Vector(0, 0), Vector(0, -10)]).line
    assert n.right
    assert not n.left


def test_init_node_2():
    segments = [
        Segment([Vector(0, 0), Vector(0, 10)]),
        Segment([Vector(0, 10), Vector(10, 10)]),
        Segment([Vector(10, 10), Vector(0, 0)])
    ]
    n = Node()
    n.build(segments)
    assert n is not None

    assert len(n.segments) == 1
    assert n.line == Segment([Vector(0, 0), Vector(0, 10)]).line
    assert not n.right
    assert n.left


def test_some_node_stuff():
    n = Node()
    segments = [
        Segment([Vector(-15, -30), Vector(-30, -30)]),
        Segment([Vector(-10, -30), Vector(-15, -30)]),
        Segment([Vector(-10, -15), Vector(-10, -30)]),
        Segment([Vector(-30, -10), Vector(-15, -10)]),
        Segment([Vector(-30, -30), Vector(-30, -10)])
    ]

    n.build(segments)


def test_some_node_stuff_2():
    n = Node()
    segments = [
        Segment([Vector(-15.0, -30.0), Vector(-30, -30)]),
        Segment([Vector(-10, -30), Vector(-15.0, -30.0)]),
        Segment([Vector(-10.0, -15.0), Vector(-10, -30)]),
        Segment([Vector(-30, -10), Vector(-15.0, -10.0)]),
        Segment([Vector(-30, -30), Vector(-30, -10)])
    ]

    n.build(segments.copy())


def test_node_clone():
    segments = [
        Segment([Vector(0, 0), Vector(0, 10)]),
        Segment([Vector(0, 10), Vector(10, 10)]),
        Segment([Vector(10, 10), Vector(0, 0)])
    ]
    n = Node(segments)

    m = n.clone()

    assert m == n
    assert m is not n
