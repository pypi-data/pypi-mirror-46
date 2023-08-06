from microlab.data.signals import Signal_1D, Signal_2D
from microlab.data.interpolation import Cubic
from microlab.data import samples


def test_interpolation_cubic_from_1D_signal():
    print(' Interpolation a Signal', end='.....')
    signal_1 = Signal_1D(values=samples.List_a, serialized=True, verbose=True)
    total_numbers = 100
    cubic_1d = Cubic(signal=signal_1, total_number=total_numbers, verbose=False)
    cubic_1d.show(title="Cubic interpolation 1D", marker='.')
    if len(cubic_1d.y) == total_numbers and len(cubic_1d.x) == total_numbers:
        print('[OK]')
    else:
        print('[!!]')

def test_interpolation_cubic_from_2D_signal():
    print(' Interpolation a Signal', end='.....')
    signal_1 = Signal_2D(values=samples.dataset_list, verbose=True)
    total_numbers = 100
    cubic_2d = Cubic(signal=signal_1, total_number=total_numbers, verbose=False)
    cubic_2d.show(title="Cubic interpolation 2D", marker='.')
    if len(cubic_2d.y) == total_numbers and len(cubic_2d.x) == total_numbers:
        print('[OK]')
    else:
        print('[!!]')

if __name__ == "__main__":
    print('\n ~ TEST 1D SIGNALS ~')
    test_interpolation_cubic_from_1D_signal()
    test_interpolation_cubic_from_2D_signal()
