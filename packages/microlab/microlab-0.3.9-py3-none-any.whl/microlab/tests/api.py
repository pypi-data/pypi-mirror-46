from microlab.signals import Signal_1D, Signal_2D, Intersection, Interpolation_Cubic
from microlab.tests import Data

# Data
# Data.show()

# 1D Signals
# signal_1 = Signal_1D(values=Data.x1, serialized=False, verbose=False)
# signal_2 = Signal_1D(values=Data.x2, serialized=False, verbose=False)
# signal_1.show(title='Signal 1 using "x1" data', marker='o')
# signal_2.show(title='Signal 2 using "x2" data', marker='o')

# 2D Signals
signal_1 = Signal_2D(values=Data.dataset_1, verbose=False)
signal_2 = Signal_2D(values=Data.dataset_2, verbose=False)
# signal_1.show(title='signal 1 using "x1" and "y1" data', marker='-')
# signal_2.show(title='signal 2 using "x2" and "y2" data', marker='-')


# Intersection
intersections = Intersection(signal_a=signal_1, signal_b=signal_2, verbose=False)
if len(intersections.points) > 0:
    intersections.show(title='intersection node ', marker='or')

# interpolation
s1 = Signal_1D(values=signal_1.x, serialized=True, verbose=False)
i1 = Interpolation_Cubic(signal=s1, total_number=10, verbose=False)
s1_interpolated = Signal_2D(values=i1.values,  verbose=True)
s1_interpolated.show(title='s1 Interpolated" ', marker='.')


s2_1d = Signal_1D(values=signal_2.x, serialized=True, verbose=True)
i2 = Interpolation_Cubic(signal=s2_1d, total_number=10, verbose=False)
s2_interpolated = Signal_2D(values=i2.values, verbose=True)
s2_interpolated.show(title='s2 Interpolated ', marker='.')





intersections = Intersection(signal_a=s1_interpolated, signal_b=s2_interpolated, verbose=True)
if len(intersections.points) > 0 :
    intersections.show(title='intersection node ', marker='or')
