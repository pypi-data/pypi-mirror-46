from matplotlib.pylab import plt


class Plot_1D:
    data = []

    def __init__(self, signal=None, title='Plot 1D', fontsize=16):
        if not signal is None:
            self.signal = signal
            self.figure = plt.figure()
            self.figure.suptitle(title, fontsize=fontsize)
            plt.plot(self.signal.x, self.signal.y, '-')
            plt.show()

    def timelapse(self, table):
        t = []
        for i in range(len(table)):
            t.append(i)
        return t


class Plot_2D:

    def __init__(self, signal=None, title='Plot 2D', fontsize=16):
        if not signal is None:
            self.signal = signal
            self.figure = plt.figure()
            self.figure.suptitle(title, fontsize=fontsize)
            plt.plot(self.signal.x, self.signal.y, '-')
            plt.show()

    def timelapse(self, table):
        t = []
        for i in range(len(table)):
            t.append(i)
        return t
