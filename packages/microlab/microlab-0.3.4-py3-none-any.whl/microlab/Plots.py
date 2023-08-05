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
