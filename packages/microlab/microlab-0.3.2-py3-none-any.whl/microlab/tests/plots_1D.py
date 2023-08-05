from microlab.Signals import Signal_1D
from microlab.Plots import Plot_1D
from microlab.tests import Data
from microlab.Types import is_1d_signal

def test_plot_1d_list():
    print('1D List -> 1D Signal  ->  1D Plot', end='.....')
    signal_1_from_list = Signal_1D(values=Data.List_a, verbose=True)

    if is_1d_signal(object=signal_1_from_list):
        print('[OK]')
        p1 = Plot_1D(title='Plot 1D List', signal=signal_1_from_list)
    else:
        print('[!!]')

def test_plot_1d_tuple():
    print('1D Tuple -> 1D Signal  ->  1D Plot', end='.....')
    signal_1_from_list = Signal_1D(values=Data.Tuple_a, verbose=True)
    if is_1d_signal(object=signal_1_from_list):
        print('[OK]')
        p1 = Plot_1D(title='Plot 1D Tuple', signal=signal_1_from_list)
    else:
        print('[!!]')


def test_plot_1d_npArray(verbose=False):
    print('1D Numpy Array -> 1D Signal  ->  1D Plot', end='.....')
    signal_1_from_list = Signal_1D(values=Data.npArray_a, verbose=True)
    if is_1d_signal(object=signal_1_from_list):
        print('[OK]')
        p1 = Plot_1D(title='Plot 1D Numpy Array', signal=signal_1_from_list)
    else:
        print('[!!]')


if __name__ == "__main__":
    print('\n ~ TEST 1D PLOT ~')
    # print('\nData: \n   A:{}, \n   B:{}'.format(Data.a, Data.b))
    test_plot_1d_list()
    test_plot_1d_tuple()
    test_plot_1d_npArray()

