from microlab.Signals import Signal_1D, Signal_2D, Interpolation_Cubic
from microlab.tests import Data
from microlab.Plots import Plot_2D

def test_interpolation_cubic_from_1D_signal():
    print(' Interpolation a Signal', end='.....')
    signal_1 = Signal_1D(values=Data.List_a, verbose=True)
    total_numbers = 100
    cubic_1d = Interpolation_Cubic(name='Cubic 1D', signal=signal_1, total_number=total_numbers, verbose=False)
    p = Plot_2D(title='Cubic 1D', signal=cubic_1d, marker='.')
    if len(cubic_1d.y) == total_numbers and len(cubic_1d.x) == total_numbers:
        print('[OK]')
    else:
        print('[!!]')

def test_interpolation_cubic_from_2D_signal():
    print(' Interpolation a Signal', end='.....')
    signal_1 = Signal_2D(values=Data.dataset_list, verbose=True)
    total_numbers = 100
    cubic_2d = Interpolation_Cubic(name='Cubic 2D', signal=signal_1, total_number=total_numbers, verbose=False)
    p = Plot_2D(title='Cubic 2D', signal=cubic_2d, marker='.')
    if len(cubic_2d.y) == total_numbers and len(cubic_2d.x) == total_numbers:
        print('[OK]')
    else:
        print('[!!]')

if __name__ == "__main__":
    print('\n ~ TEST 1D SIGNALS ~')
    # print('\nData: \n   A:{}, \n   B:{}'.format(Data.a, Data.b))
    test_interpolation_cubic_from_1D_signal()
    test_interpolation_cubic_from_2D_signal()
