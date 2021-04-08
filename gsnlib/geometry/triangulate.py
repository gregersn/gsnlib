from typing import List, Union, Any
from . import Shape, Polygon, Vector


def triangulate(input: Union[Shape, Polygon]) -> List[Polygon]:
    polygons = []
    if isinstance(input, Polygon):
        if len(input.points) == 3:
            return [input, ]

        points: List[Vector] = []
        for p in input.points:
            points.append(p)

        pos = 0
        while len(points) > 3:
            vi = points[pos]
            vin = points[pos + 1]
            vip = points[(len(points) + pos - 1) % len(points)]
            cur_poly = Polygon([vi, vin, vip])

            ear = True
            for point in points[pos + 2:-1]:
                if cur_poly.contains(point):
                    ear = False
                    break

            if ear:
                polygons.append(cur_poly)
                points.pop(pos)
                pos = 0
            else:
                pos += 1

        if len(points) == 3:
            polygons.append(Polygon(points))

    return polygons
