from scipy.interpolate import interp1d


class Signal_1D:
    data = []

    def __init__(self, data=None):

        if not data is None:
            self.data = data



class Signal_2D:

    def __init__(self, data=None):
        pass




class Interpolation:

    def __init__(self,signal):
        pass


class Intersection:

    def __init__(self, signal_a=None, signal_b=None):

        if signal_a is None or signal_b is None:
            print(' Signals is required')
        else:
            self.signal_a = signal_a
            self.signal_b = signal_b

