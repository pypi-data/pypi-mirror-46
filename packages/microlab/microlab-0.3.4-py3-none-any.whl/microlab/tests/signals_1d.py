from microlab.Signals import Signal_1D,Signal_2D, Interpolation_Cubic
from microlab.Plots import Plot_1D
from microlab.tests import Data
from microlab.Types import is_1d_signal

def test_from_list_to_signal():
    print('List   ->  Signal', end='.....')
    signal_1_from_list = Signal_1D(values=Data.List_a, verbose=True)
    if is_1d_signal(object=signal_1_from_list):
        print('[OK]')
        signal_1_from_list.show_cordinates()
    else:
        print('[!!]')

def test_from_tuple_to_signal():
    print('Tuple  ->  Signal', end='.....')
    signal_1_from_tuple = Signal_1D(values=Data.Tuple_a, verbose=True)
    if is_1d_signal(object=signal_1_from_tuple):
        print('[OK]')
        signal_1_from_tuple.show_cordinates()
    else:
        print('[!!]')

def test_from_nmArray_to_signal():
    print('Array  ->  Signal', end='.....')
    signal_1_from_npArray = Signal_1D(values=Data.npArray_a, verbose=True)
    if is_1d_signal(object=signal_1_from_npArray):
        print('[OK]')
        signal_1_from_npArray.show_cordinates()
    else:
        print('[!!]')


if __name__ == "__main__":
    print('\n ~ TEST 1D SIGNALS ~')
    # print('\nData: \n   A:{}, \n   B:{}'.format(Data.a, Data.b))
    test_from_list_to_signal()
    test_from_tuple_to_signal()
    test_from_nmArray_to_signal()



