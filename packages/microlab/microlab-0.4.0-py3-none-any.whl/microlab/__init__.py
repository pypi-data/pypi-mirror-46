import os
import sys

__version__ = "0.4.0"

path = ''

def start_test(ip='0', port=8000):
    '''
                Start the wb application service
    '''
    if sys.platform == 'linux':
        path = "/".join(os.path.abspath(__file__).split("/")[:-1])
        print('[ microlab ]  starting web app on linux')

    else:
        path = "\\".join(os.path.abspath(__file__).split("\\")[:-1])
        print('[ microlab ]  starting web app on windows')
    examples = os.path.join(path, 'examples')
    #sys.path.append(path)
    #print(sys.path)
    #web_app = os.path.join(path, 'app', 'manage.py')
    #os.system('python3 {} runserver {}:{}'.format(web_app, ip, port))    
    #self_test = os.path.join(path, 'self_test')
    print('microlab found at {}'.format(path))
    print('examples found at {}'.format(examples))

    os.system('cd {} && python3 io/file_C.R.U.D.py '.format(examples))


