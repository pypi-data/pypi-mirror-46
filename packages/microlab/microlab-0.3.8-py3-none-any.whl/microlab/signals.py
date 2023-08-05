from __future__ import print_function

from numpy import ndarray, linspace, asarray
from scipy.interpolate import interp1d
from microlab.plots import Plot_1D, Plot_2D, Plot_Intersection
from microlab.geometry import create_line
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

    def __init__(self, values=[], serialized=False, verbose=False):
        if values is None:
            print('[!] cannot create a 1D Signal with None values. ')

        # input values is list
        elif type(values) in [list]:
            if serialized:
                self.x = []
                self.y = []
                for x, y in enumerate(values):
                    self.x.append(x)
                    self.y.append(y)
            else:
                self.x = values
                self.y = self.timelapse(table=values)
            if verbose:
                print('[ List    ]---->| {} [ X: {}, Y:{} ]'.format(type(self), len(self.x), len(self.y)))
                # print(self.x)
                # print(self.y)

        # input values is tuple
        elif type(values) in [tuple]:
            if serialized:
                for x, y in enumerate(values):
                    self.x.append(x)
                    self.y.append(y)
            else:
                self.x = values
                self.y = self.timelapse(table=values)
            if verbose:
                print('[ Tuple   ]---->| {} [ X: {}, Y:{} ]'.format(type(self), len(self.x), len(self.y)))

        # input values is ndarray
        elif type(values) in [ndarray]:
                self.x = asarray(values)
                self.y = self.timelapse(table=values)

                if verbose:
                    print('[ ndArray ]---->| {} [ X: {}, Y:{} ]'.format(type(self), len(self.x), len(self.y)))

        # create signal values
        self.values = [self.x, self.y]

    def timelapse(self, table):
        t = []
        for i in range(len(table)):
            t.append(i)
        return t

    def show_coordinates(self):
        print('X: {}'.format(self.x))
        print('Y: {}'.format(self.y))

    def show(self, title='Signal 1D', marker='.'):
        Plot_1D(signal=self, title=title, marker=marker)


class Signal_2D:
    x = []
    y = []
    values = [x, y]

    def __init__(self, values=[], time=None, verbose=False):
        if values is None:
            print('[!] cannot create a 2D Signal with None values. ')

        # values has this shape [ [x1, x2], [y1, y2] ]
        if len(values) == 2:
            self.values = values
            self.y = values[0]
            self.x = values[1]

        # values has this shape [x1, x2, x3]
        # time   has this shape [y1, y2, y3]
        elif not time is None:
            self.y = values
            self.x = time

        #  values are tuple or list
        if type(values) in [tuple, list]:
            if verbose:
                print('[ List or Tuple ]->| {} [ X: {}, Y:{} ]'.format(type(self), len(self.x), len(self.y)))

        #  values are ndarrays
        elif type(values) in [ndarray]:
            if verbose:
                print('[ ndArray ]---->| {} [ X: {}, Y:{} ]'.format(type(self), len(self.x), len(self.y)))

        self.values = [self.x, self.y]

    def show_coordinates(self):
        print('X: {}'.format(self.x))
        print('Y: {}'.format(self.y))

    def show(self, title='Signal 2D', marker='.'):
        Plot_2D(signal=self, title=title, marker=marker)


class Interpolation_Cubic:
    x = []
    y = []
    values = [x, y]
    def __init__(self, signal=None, total_number=10, verbose=False):
        if signal is None:
            print('[!] can not interpolate None signal')
        elif type(signal) == Signal_1D:
            self.signal = signal
            x = self.signal.x
            y = self.signal.y
            self.x, self.y = self.cubic(x, y, total_number, verbose=verbose)
            # if verbose:
            #     print('Signal 1D found')
            #     print('New    X:{}'.format(len(self.x)))
            #     print('New    Y:{}'.format(len(self.y)))

        elif type(signal) == Signal_2D:
            self.signal = signal
            x = self.signal.x
            y = self.signal.y
            self.x, self.y = self.cubic(x, y, total_number, verbose=True)
            if verbose:
                print('Signal 2D found')
                print('New    X:{}'.format(len(self.x)))
                print('New    Y:{}'.format(len(self.y)))
        self.values = [self.x, self.y]

    def cubic(self, x, y, total_number, verbose=False):
        multiplier = total_number / len(x)
        if verbose:
            print(' Cubic interpolation', end=' ')
            print('X: {}, Y: {}'.format(x, y))

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

    def show_coordinates(self):
        print('X: {}'.format(self.x))
        print('Y: {}'.format(self.y))

    def show(self, title='Interpolation', marker='.'):
        Plot_2D(signal=self, title=title, marker=marker)


class Intersection:
    coordinates = [[], []]
    points = []

    def __init__(self, name='' , signal_a=Signal_2D(), signal_b=Signal_2D(), verbose=False):
        self.name = name

        if signal_a is None or signal_b is None:
            print(' Signals is required')
        else:
            self.signal_a = signal_a
            self.signal_b = signal_b
            self.line_a = create_line(signal=self.signal_a, verbose=False)
            self.line_b = create_line(signal=self.signal_b, verbose=False)
            self.points = self.find_intersect_points(verbose=verbose)

    def show_coordinates(self):
        print('[ {}   Intersection'.format(self.name))
        for i, intersection in enumerate(self.coordinates):
            if i == 0:
                print(' X: {}'.format(intersection))
            elif i == 1:
                print(' Y: {}'.format(intersection))

    def show(self, title='Intersection', marker='o'):
        Plot_Intersection(intersection=self, title=title, marker=marker)


    def find_intersect_points(self, verbose=False):
        self.coordinates = [[], []]
        intersection_result = self.line_a.intersection(self.line_b)
        # print('res: {}'.format(res))

        self.points = []
        try:
            # more than one points found
            if len(intersection_result):
                if verbose:
                    print('{} signals has {} intersected points  '.format(self.name,len(intersection_result)))

            # iterate in points
            for point in intersection_result:

                # collect point
                self.points.append(point)
                x, y = point.xy

                # collect coordinates
                self.coordinates[0].append(x)
                self.coordinates[1].append(y)

                # if verbose:
                #     print('+ {}'.format(point), type(point))

        except:
            """ Only one intersection point found """
            if verbose:
                print('one intersection point found')

            # collect point
            point = intersection_result
            self.points.append(point)

            # collect coordinates
            x, y = point.xy
            self.coordinates[0].append(x)
            self.coordinates[1].append(y)

            if verbose:
                print('+ {}'.format(point), type(point))
        return self.points

