from microlab.Signals import Intersection
from microlab.Signals import Signal_2D
from microlab.tests import Data


def test_intersection_from_2D_signal():
    print(' Intersection from 2 Signals 2D', end='.....')

    # Signals
    signal_1 = Signal_2D(values=Data.dataset_1, verbose=False)
    signal_2 = Signal_2D(values=Data.dataset_2, verbose=False)

    # Intersection
    intersection = Intersection(signal_a=signal_1, signal_b=signal_2, verbose=True)
    # intersection.show()
    # print(intersection.points)
    if len(intersection.points) > 1:
        print('[OK]')
    else:
        print('[!!]')




if __name__ == "__main__":
    print('\n ~ TEST INTERSECTION ~')
    # print('\nData: \n   A:{}, \n   B:{}'.format(Data.a, Data.b))
    test_intersection_from_2D_signal()


