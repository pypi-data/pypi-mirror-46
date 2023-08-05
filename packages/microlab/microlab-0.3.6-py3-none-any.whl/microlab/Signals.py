from __future__ import print_function

from numpy import ndarray, linspace
from scipy.interpolate import interp1d
from shapely.geometry import LineString, Polygon
from microlab.Plots import Plot_1D, Plot_2D, Plot_Intersection
from matplotlib import pyplot as plt

types = [
            tuple,
            list,
            ndarray
        ]



class Signal_1D:
    x = []
    y = []
    values = [x, y]

    def __init__(self, values=None, serialized=False, verbose=False):
        if values is None:
            print('[!] cannot create a Signal with None data. ')
        elif type(values) in [list]:
            if serialized:
                for x, y in enumerate(values):
                    self.x.append(x)
                    self.y.append(y)
            else:
                self.x = values
                self.y = self.timelapse(table=values)

        elif type(values) in [ndarray]:
                self.x = values[0]
                self.y = values[1]
        self.values = [self.x, self.y]

    def timelapse(self,table):
        t = []
        for i in range(len(table)):
            t.append(i)
        return t

    def show_cordinates(self):
        print('X: {}'.format(self.x))
        print('Y: {}'.format(self.y))

    def show(self, title='Signal 1D', marker='.'):
        Plot_1D(signal=self, title=title, marker=marker)


class Signal_2D:
    x = []
    y = []
    values = [x, y]

    def __init__(self, values=None, time=None, verbose=False):
        if not values is None:
            if len(values) == 2 and type(values) in types:
                self.values = values
                self.x = values[0]
                self.y = values[1]
            elif not time is None:
                self.x = values
                self.y = time
            self.values = [self.x, self.y]

    def show_cordinates(self):
        print('X: {}'.format(self.x))
        print('Y: {}'.format(self.y))

    def show(self, title='Signal 2D', marker='.'):
        Plot_2D(signal=self, title=title, marker=marker)


class Interpolation_Cubic:

    def __init__(self, signal=None, total_number=10, verbose=False):
        if signal is None:
            print('[!] can not interpolate None signal')
        elif type(signal) == Signal_1D:
            print('start')
            self.signal = signal
            x = self.signal.x
            y = self.signal.y
            print('x inside: {}'.format(x))
            print('y inside: {}'.format(y))
            self.x , self.y = self.cubic(x, y, total_number, verbose=True)

        elif type(signal) == Signal_2D:
            print('start')
            self.signal = signal
            x = self.signal.x
            y = self.signal.y
            print('x inside: {}'.format(x))
            print('y inside: {}'.format(y))
            self.x , self.y = self.cubic(x, total_number, verbose=True)

    def cubic(self, x, y, total_number, verbose=False):
        multiplier = total_number / len(x)
        if verbose:
            print(' Cubic interpolation', end=' ')
        xnew = self.generate_new_frames(x, multiplier)
        f = interp1d(x, y, kind='cubic')
        ynew = f(xnew)
        ynew = ynew.tolist()
        return xnew, ynew

    def generate_new_frames(self, x, multiplier, verbose=False):
        total_points = len(x) * multiplier
        xnew = linspace(0, len(x) - 1, num=total_points, endpoint=True)
        if verbose:
            print('generated {} frames '.format(total_points - len(x)))
        return xnew

    def show_cordinates(self):
        print('X: {}'.format(self.x))
        print('Y: {}'.format(self.y))

    def show(self, title='Interpolation', marker='.'):
        Plot_2D(signal=self, title='aaaa', marker=marker)


class Intersection:

    def __init__(self, signal_a=None, signal_b=None, verbose=False):

        if signal_a is None or signal_b is None:
            print(' Signals is required')

        else:
            self.signal_a = signal_a
            self.signal_b = signal_b
            self.line_a = self.create_line(signal=self.signal_a, verbose=verbose)
            self.line_b = self.create_line(signal=self.signal_b, verbose=verbose)
            self.points = self.find_intersect_points(verbose=verbose)

    def show_cordinates(self):
        for i, intersection in enumerate(self.intersections):
            print(' intersection {} : {}'.format(i + 1, intersection))

    def show(self, title='Intersection', marker='o'):
        Plot_Intersection(intersection=self, title=title, marker=marker)

    def create_line(self, signal, verbose=False):
        x_values = signal.x
        y_values = signal.y
        if verbose:
            print('Line', 'X:', len(x_values), 'Y:', len(y_values), end='')
        points = []
        for x, y in zip(x_values, y_values):
            point = (x, y)
            points.append(point)
        if verbose:
            print(LineString(points))
        return LineString(points)

    def find_intersect_points(self, verbose=False):
        points = [[], []]
        res = self.line_a.intersection(self.line_b)
        # print('res: {}'.format(res))
        xy = res.xy
        if len(xy) == 2:
            x, y = xy[0], xy[1]
            if verbose:
                print('found: {} intersection point {}'.format(int(len(xy) / 2), (x[0],y[0])))
            points[0].append(x)
            points[1].append(y)
        else:
            if verbose:
                print('found: {}'.format(int(len(res.xy) / 2)))
            for point in res:
                x, y = point.xy
                points[0].append(x)
                points[1].append(y)
        return points

