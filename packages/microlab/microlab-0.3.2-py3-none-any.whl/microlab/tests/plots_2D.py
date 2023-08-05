from microlab.Signals import Signal_2D
from microlab.Plots import Plot_2D
from microlab.tests import Data
from microlab.Types import is_2d_signal

def test_plot_1d_list():
    print('2D List -> 2D Signal  ->  2D Plot', end='.....')
    signal_1_from_list = Signal_2D(values=Data.dataset_list, verbose=True)

    if is_2d_signal(object=signal_1_from_list):
        print('[OK]')
        p1 = Plot_2D(title='Plot 2D List', signal=signal_1_from_list)
    else:
        print('[!!]')

def test_plot_1d_tuple():
    print('2D Tuple -> 2D Signal  ->  2D Plot', end='.....')
    signal_1_from_list = Signal_2D(values=Data.dataset_tuple, verbose=True)
    if is_2d_signal(object=signal_1_from_list):
        print('[OK]')
        p1 = Plot_2D(title='Plot 2D Tuple', signal=signal_1_from_list)
    else:
        print('[!!]')


def test_plot_1d_npArray(verbose=False):
    print('2D Numpy Array -> 2D Signal  ->  2D Plot', end='.....')
    signal_1_from_list = Signal_2D(values=Data.dataset_npArray, verbose=True)
    if is_2d_signal(object=signal_1_from_list):
        print('[OK]')
        p1 = Plot_2D(title='Plot 2D Numpy Array', signal=signal_1_from_list)
    else:
        print('[!!]')


if __name__ == "__main__":
    print('\n ~ TEST 2D PLOT ~')
    # print('\nData: \n   A:{}, \n   B:{}'.format(Data.a, Data.b))
    test_plot_1d_list()
    test_plot_1d_tuple()
    test_plot_1d_npArray()

