from microlab.Signals import Signal_2D
from microlab.Plots import Plot_2D
from microlab.tests import Data
from microlab.Types import is_2d_signal


def test_from_list_to_signal():
    print('List   ->  Signal', end='.....')
    signal_1_from_list = Signal_2D(values=Data.dataset_list, verbose=True)
    if is_2d_signal(object=signal_1_from_list):
        print('[OK]')
        signal_1_from_list.show_cordinates()
    else:
        print('[!!]')


def test_from_tuple_to_signal():
    print('Tuple  ->  Signal', end='.....')
    signal_1_from_tuple = Signal_2D(values=Data.dataset_tuple, verbose=True)
    if is_2d_signal(object=signal_1_from_tuple):
        print('[OK]')
        signal_1_from_tuple.show_cordinates()
    else:
        print('[!!]')

def test_from_nmArray_to_signal():
    print('Numpy  ->  Signal', end='.....')
    signal_1_from_ndArray = Signal_2D(values=Data.dataset_npArray, verbose=True)
    if is_2d_signal(object=signal_1_from_ndArray):
        print('[OK]')
        signal_1_from_ndArray.show_cordinates()
    else:
        print('[!!]')


if __name__ == "__main__":
    print('\n ~ TEST 2D SIGNALS ~')
    # print('\nData: \n   A:{}, \n   B:{}'.format(Data.a, Data.b))
    test_from_list_to_signal()
    test_from_tuple_to_signal()
    test_from_nmArray_to_signal()



