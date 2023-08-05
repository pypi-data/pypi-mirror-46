from numpy import ndarray, linspace
from scipy.interpolate import interp1d


types = [
            tuple,
            list,
            ndarray
        ]


class Signal_1D:
    x = []
    y = []
    values = [y]

    def __init__(self, values=None, verbose=False):
        # validate the type of values
        if values is None:
            print('[!] cannot create a Signal with None data. ')
        elif type(values) in [list]:
            self.values = values
            for x, y in enumerate(values):
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
            if len(values) == 2 and type(values) in types:
                self.values = values
                self.x = values[0]
                self.y = values[1]

    def show_cordinates(self):
        print('X: {}'.format(self.x))
        print('Y: {}'.format(self.y))


class Interpolation_Cubic:

    def __init__(self, name = '', signal=None, total_number=10, verbose=False):
        if signal is None:
            print('[!] can not interpolate None signal')

    # elif type(self.signal) == Signal_1D:
        self.signal = signal
        x = self.signal.x
        y = self.signal.y

        multiplier = total_number / len(x)
        if verbose:
            print('[{}] Cubic interpolation for {} points '.format(name ,total_number), end=' ')
        self.x = self.generate_new_frames(multiplier, verbose=verbose)
        f = interp1d(x, y, kind='cubic')
        ynew = f(self.x)
        self.y = ynew.tolist()


    def generate_new_frames(self, multiplier, verbose=False):
        x = self.signal.x
        total_points = len(x) * multiplier
        xnew = linspace(0, len(x) - 1, num=total_points, endpoint=True)
        if verbose:
            print('generated {} frames '.format(total_points - len(x)))
        return xnew

    def show_cordinates(self):
        print('X: {}'.format(self.x))
        print('Y: {}'.format(self.y))


class Intersection:

    def __init__(self, signal_a=None, signal_b=None):

        if signal_a is None or signal_b is None:
            print(' Signals is required')
        else:
            self.signal_a = signal_a
            self.signal_b = signal_b

