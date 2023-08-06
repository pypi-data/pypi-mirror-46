import os
import sys
from microlab.io.yaml import create_yaml, read_yaml
from microlab.io.files import delete_file

''' BRAIN '''
__version__ = "0.4.1"
debug = True
memory = {
        'path': None,
        'examples': None,
        }


# wake up
if sys.platform == 'linux':
    memory['path'] = "/".join(os.path.abspath(__file__).split("/")[:-1])
else:
    memory['path'] = "\\".join(os.path.abspath(__file__).split("\\")[:-1])

memory['examples'] = os.path.join(memory['path'], 'examples')


''' STRUCTURE  '''
tests = {

        'file': os.path.join(memory['examples'], 'io', 'file_C.R.U.D.py'),
        'json': os.path.join(memory['examples'], 'io', 'json_C.R.U.D.py'),
        'csv': os.path.join(memory['examples'], 'io', 'csv_C.R.U.D.py'),
        'yaml': os.path.join(memory['examples'], 'io', 'yaml_C.R.U.D.py'),
        'zip': os.path.join(memory['examples'], 'io', 'yaml_C.R.U.D.py'),
        'signal 1-D': os.path.join(memory['examples'], 'signals', '1d.py'),
        'signal 2-D': os.path.join(memory['examples'], 'signals', '2d.py'),
        'interpolation': os.path.join(memory['examples'], 'signals', 'interpolation.py'),
        'intersection': os.path.join(memory['examples'], 'signals', 'Intersection.py'),

        'symetric': os.path.join(memory['examples'], 'cryptography', 'symmetric.py'),
        'asymetric': os.path.join(memory['examples'], 'cryptography', 'asymmetric.py'),
        }
apps = {}
lab = {'name': 'new lab',
       'version': '0.1',
       'path': os.getcwd()}

# find lab
try:
    lab_file = read_yaml(path='lab', verbose=False)
    memory = lab_file['memory']
    lab = lab_file['lab']
    tests = lab_file['tests']
    apps = lab_file['apps']
    if debug:
        print('[ {} ]   lab loaded'.format(lab['name']))
        print('[ {} ]   memory loaded'.format(lab['name']))
        print('[ {} ]   tests loaded'.format(lab['name']))
        print('[ {} ]   apps loaded'.format(lab['name']))
except Exception as e:
    if debug:
        print('[ {} ]   no lab found'.format(lab['name']))
        print(e)


def help():
    print(' status ')

    print(' show_test ')
    print(' show_apps ')

    print(' add_test ')
    print(' add_apps ')

    print(' start_app ')

    print(' reload_lab ')
    print(' save_lab ')

    print(' change_name ')
    print(' change_version ')


def status():
    print('[ {} ]  v {}'.format(lab['name'], lab['version']))
    print('[ {} ]   apps: {}'.format(lab['name'], apps.keys().__len__()))


# show
def show_tests():
    for test_name, test_path in tests.items():
        print('[  {}  ]     {}'.format(test_name, test_path))


def show_apps():
    for app_name , app in apps.items():
        print('[  {}  ]  '.format(app_name))
        for field, value in app.items():
            print('     {} : {}'.format(field, value))


# create
def save_lab():
    create_yaml(path='lab',
                data={'lab': lab,
                      'memory': memory,
                      'tests': tests,
                      'apps': apps},
                verbose=False)


# read
def reload_lab():
    try:
        lab_file = read_yaml(path='lab', verbose=False)
        memory = lab_file['memory']
        lab = lab_file['lab']
        tests = lab_file['tests']
        apps = lab_file['apps']

        print('[ {} ]   lab loaded'.format(lab['name']))
        print('[ {} ]   memory loaded'.format(lab['name']))
        print('[ {} ]   tests loaded'.format(lab['name']))
        print('[ {} ]   apps loaded'.format(lab['name']))

    except Exception as e:
        create_yaml(path='lab',
                    data={'lab': lab,
                          'memory': memory,
                          'tests': tests,
                          'apps': apps},
                    verbose=False)

        print('[ {} ]   new lab created'.format(lab['name']))
        print(e)


# update
def change_name(name):
    lab['name'] = name
    save_lab()


def change_version(version):
    lab['version'] = version
    save_lab()


def add_app(name, directory, script, parameters=''):
    apps[name] = {'directory': directory,
                 'script': script,
                 'parameters': parameters}
    save_lab()


def add_test(name, directory):
    tests[name] = directory
    save_lab()


# actions
def run_app(app):
    '''
                    start apps inside microlab
    :param file:
    :return:
    '''

    if sys.platform == 'linux':
        full_path = os.path.join(app['directory'], app['script'])
        command = 'python3 {} {}'.format(full_path, app['parameters'])
    else:
        os.chdir(app['directory'])
        command = 'python {} {}'.format(app['script'], app['parameters'])
    print('COMMAND: {}'.format(command))
    os.system(command)


def run_python(file):
    '''
                    execute .py files inside microlab
    :param file:
    :return:
    '''
    os.system('python3 {} '.format(file))


def start_tests():
    '''
                Start the wb application service
    '''
    for test_name, test_python_scrypt in tests.items():
        run_python(file=test_python_scrypt)


def start_app(app_name=''):
    '''
                Start the wb application service
    '''
    print('[  {}  ]     {}'.format(app_name, apps[app_name]))
    run_app(app=apps[app_name])





