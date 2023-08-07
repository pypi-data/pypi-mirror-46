from microlab.data.signals import Signal_2D
from microlab.data.samples import dataset_npArray

from microlab.geometry.points import create_points, Point


if __name__ == '__main__':
    signal = Signal_2D(values=dataset_npArray, verbose=False)
    points = create_points(signal=signal, verbose=True)
    print(points)
