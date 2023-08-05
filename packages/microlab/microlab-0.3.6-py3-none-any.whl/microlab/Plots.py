from matplotlib.pylab import plt


class Plot_1D:
    data = []

    def __init__(self, signal=None, title='Plot 1D', fontsize=16, marker='.'):
        if not signal is None:
            self.signal = signal
            x=self.signal.x
            y=self.signal.y
            self.figure = plt.figure()
            self.figure.suptitle(title+'(x:{}, y:{})'.format(len(x), len(y)), fontsize=fontsize)
            plt.plot(x, y, marker)
            plt.show()


class Plot_2D:

    def __init__(self, signal=None, title='Plot 2D', fontsize=16, marker='.'):
        if not signal is None:
            self.signal = signal
            x=self.signal.x
            y=self.signal.y
            self.figure = plt.figure()
            self.figure.suptitle(title+'(x:{}, y:{})'.format(len(x), len(y)), fontsize=fontsize)
            plt.plot(x, y, marker)
            plt.show()


class Plot_Intersection:

    def __init__(self, intersection, title='Plot Intersection', fontsize=16, marker='.'):
        self.figure = plt.figure()
        self.figure.suptitle(title, fontsize=fontsize)
        self.intersection = intersection
        self.plot_line(line=self.intersection.line_a)
        self.plot_line(line=self.intersection.line_b)
        self.plot_points(points=self.intersection.points, marker=marker)
        plt.show()

    def plot_line(self, line, marker='-'):
        x, y = line.xy
        plt.plot(x, y, marker)

    def plot_point(self, point, marker='.'):
        x, y = point.xy
        plt.plot(x, y, marker)

    def plot_points(self,points, marker='.'):
        x, y = points[0], points[1]
        plt.plot(x, y, marker)


