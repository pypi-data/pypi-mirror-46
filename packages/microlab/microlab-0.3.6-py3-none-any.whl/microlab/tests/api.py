from microlab.Signals import Signal_1D, Signal_2D, Intersection, Interpolation_Cubic
from microlab.tests import Data


# Data
Data.show()

# 1D Signals
signal_1 = Signal_1D(values=Data.x1, serialized=False, verbose=False)
signal_2 = Signal_1D(values=Data.x2, serialized=False, verbose=False)
signal_1.show(title='Signal 1 using "x1" data', marker='o')
signal_2.show(title='Signal 2 using "x2" data', marker='o')

# 2D Signals
signal_1 = Signal_2D(values=Data.dataset_1, verbose=False)
signal_2 = Signal_2D(values=Data.dataset_2, verbose=False)
signal_1.show(title='signal 1 using "x1" and "y1" data', marker='-')
signal_2.show(title='signal 2 using "x2" and "y2" data', marker='-')

# Intersection
intersection = Intersection(signal_a=signal_1, signal_b=signal_2, verbose=False)
intersection.show(title='intersection node ', marker='or')

# interpolation
s1 = Signal_1D(values=signal_2.x, serialized=True, verbose=False)
s1.show(title='New signal using x values')

i = Interpolation_Cubic(signal=s1, total_number=100, verbose=False)
i.show(title='Interpolation using "s1" data', marker='.')
