from microlab import hardware
import time


if __name__=='__main__':
    print(' ~ TEST HARDWARE \n')
    while True:
        time.sleep(1)
        hw = hardware.statistics()
        print('\r CPU: {}%  RAM: {}% '.format(hw['cpu']['percent'], hw['ram']['percent']), end=' ')
