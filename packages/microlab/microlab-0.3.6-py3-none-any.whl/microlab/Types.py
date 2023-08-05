from microlab.Signals import Signal_1D, Signal_2D


""" Microlab """
Signal_1D_type = type(Signal_1D())
Signal_2D_type = type(Signal_2D())


def is_1d_signal(object):
    if type(object) == Signal_1D_type:
        return True
    return False


def is_2d_signal(object):
    if type(object) == Signal_2D_type:
        return True
    return False
