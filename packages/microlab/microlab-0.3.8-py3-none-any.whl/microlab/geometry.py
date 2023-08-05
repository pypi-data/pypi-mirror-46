from shapely.geometry.point import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry.linestring import LineString


def create_line(signal, verbose=False):
    x_values = signal.y
    y_values = signal.x
    if verbose:
        print('Create Line |', 'X:', len(x_values), 'Y:', len(y_values), end=' | ')
    points = []
    for x, y in zip(x_values, y_values):
        point = (x, y)
        points.append(point)
    if verbose:
        print(LineString(points))
    return LineString(points)
