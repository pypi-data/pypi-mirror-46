from microlab.data.signals import Signal_2D
from microlab.data.samples import dataset_npArray
from microlab.geometry.lines import create_line


if __name__ == '__main__':
    signal = Signal_2D(values=dataset_npArray, verbose=False)
    line = create_line(signal=signal, verbose=True)
    print(line)
