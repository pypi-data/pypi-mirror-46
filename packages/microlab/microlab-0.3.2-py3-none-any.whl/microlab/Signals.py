from numpy import ndarray
from scipy.interpolate import interp1d


types = [
            tuple,
            list,
            ndarray
        ]


class Signal_1D:
    values = []
    x = []
    y = []

    def __init__(self, values=None, verbose=False):
        # validate the type of values
        if values is None:
            print('[!] cannot create a Signal with None data. ')

        elif type(values) in [list]:
            self.values = values
            for x, y in enumerate(self.values):
                self.x.append(x)
                self.y.append(y)

    def show_cordinates(self):
        print('X: {}'.format(self.x))
        print('Y: {}'.format(self.y))


class Signal_2D:
    x = []
    y = []
    values = [x, y]

    def __init__(self, values=None, verbose=False):
        # validate the type of values
        if not values is None:
            # print('len: {}'.format(len(values)))
            # print('type: {}'.format(type(values)))
            if len(values) == 2 and type(values) in types:
                self.values = values
                self.x = values[0]
                self.y = values[1]

    def show_cordinates(self):
        print('X: {}'.format(self.x))
        print('Y: {}'.format(self.y))


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

