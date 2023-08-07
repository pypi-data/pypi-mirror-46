import os
import sys
from microlab.io.yaml import create_yaml, read_yaml
from microlab.io.files import delete_file

''' BRAIN '''
debug = False
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


''' WORKSPACE STRUCTURE  '''
tests = {
        'monitoring': os.path.join(memory['examples'], 'hardware', 'monitoring.py'),
        'file': os.path.join(memory['examples'], 'io', 'file_C.R.U.D.py'),
        'json': os.path.join(memory['examples'], 'io', 'json_C.R.U.D.py'),
        'csv': os.path.join(memory['examples'], 'io', 'csv_C.R.U.D.py'),
        'yaml': os.path.join(memory['examples'], 'io', 'yaml_C.R.U.D.py'),
        'zip': os.path.join(memory['examples'], 'io', 'zip_C.R.U.D.py'),
        'signal 1-D': os.path.join(memory['examples'], 'signals', '1d.py'),
        'signal 2-D': os.path.join(memory['examples'], 'signals', '2d.py'),
        'interpolation': os.path.join(memory['examples'], 'signals', 'interpolation.py'),
        'intersection': os.path.join(memory['examples'], 'signals', 'Intersection.py'),

        'symetric': os.path.join(memory['examples'], 'cryptography', 'symmetric.py'),
        'asymetric': os.path.join(memory['examples'], 'cryptography', 'asymmetric.py'),
        }
workspace = {'name': 'Myworkspace',
            'version': '0.1',
            'path': os.getcwd(),
            'tests': {},
            'packages': {}

            }


def help(target):
    print('\n - - - - - - - - - - - - -')
    print('  Microlab Assistant v {} '.format('0.1'))
    print(' - - - - - - - - - - - - -')

    if target in ['workspace']:
        print('\n load() ')
        print(' save() ')
        print(' delete() ')

        print('\n change_name( < new name > ) ')
        print(' change_version( < new version >)')

        print('\n status() ')
        print(' show( < test > or < test name >  ,  < packages > or < package name >) ')

        print('\n add_test() ')
        print('\n start( < tests >  or  < test name > ) ')

    elif target in ['packages']:

        print('\n start(  < packages > or < package name > ) ')
    else:
        print('\n target {} is not valid'.format(target))



# load the workspace
def load():
    global workspace

    try:
        workspace_file = read_yaml(path='workspace', verbose=False)
        workspace = workspace_file['workspace']
        if debug:
            print('[ {} ]   workspace loaded'.format(workspace['name']))
            print('[ {} ]   memory loaded'.format(workspace['name']))

    except Exception as e:
        if debug:
            print('[ {} ]   no workspace found in {}'.format(workspace['name'], os.getcwd()))
            print('[ exception] {}'.format(e))


# save the workspace
def save():
    create_yaml(path='workspace',
                data={'workspace': workspace},
                verbose=False)


# clean the workspace
def clean():
    workspace['tests'] = {}
    workspace['packages'] = {}
    delete_file(path='workspace', verbose=False)


# show workspace status
def status():
    print('[ {} ]  workspace    {}'.format(workspace['name'], workspace['path']))
    print('[ {} ]  version      {}'.format(workspace['name'], workspace['version']))
    print('[ {} ]  packages     {}'.format(workspace['name'], workspace['packages'].keys().__len__()))
    print('[ {} ]  tests        {}'.format(workspace['name'], workspace['tests'].keys().__len__()))


# change workspace name
def change_name(name):
    workspace['name'] = name
    save()


# change workspace version
def change_version(version):
    workspace['version'] = version
    save()


# add new package to workspace
def add_package(name, directory, executor, arguments='', installer='install.sh', uninstaller='uninstall.sh'):
    workspace['packages'][name] = {
                          'arguments': arguments,
                          'directory': directory,
                          'executor': executor,
                          'installer': installer,
                          'uninstaller': uninstaller,
                          }
    save()


# add new test to lab
def add_test(name, directory=None):
    if directory is None:
        if name in tests:
            workspace['tests'][name] = tests[name]
    else:
        workspace['test'][name] = directory
    save()


# Show action
def show(arg):
    # show all workspace packages
    if arg in ['packages']:
        for package_name, package in workspace['packages'].items():
            print('[  {}  ]  '.format(package_name))
            for field, value in package.items():
                print('     {} : {}'.format(field, value))

    elif arg in ['tests']:
        for test_name, test_path in workspace['tests'].items():
            print('[  {}  ]     {}'.format(test_name, test_path))


# Start action
def start(arg):
    # start a workspace test
    if arg in workspace['tests']:
        test_python_scrypt = workspace['tests']
        if sys.platform == 'linux':
            os.system('python3 {} '.format(test_python_scrypt))
        else:
            os.system('python {} '.format(test_python_scrypt))

    # start all workspace tests
    elif arg in ['tests']:
        for test_name, test_python_scrypt in workspace['tests'].items():
            if sys.platform == 'linux':
                os.system('python3 {} '.format(test_python_scrypt))
            else:
                os.system('python {} '.format(test_python_scrypt))

    # start a microlab Test
    if arg in tests:
        test_python_scrypt = tests[arg]
        if sys.platform == 'linux':
            os.system('python3 {} '.format(test_python_scrypt))
        else:
            os.system('python {} '.format(test_python_scrypt))

    # start an package
    elif arg in workspace['packages']:
        package_name = arg
        package = workspace['packages'][package_name]
        print('[  {}  ]     is starting'.format(package_name))
        if sys.platform == 'linux':
            full_path = os.path.join(package['directory'], package['executor'])
            command = 'python3 {} {}'.format(full_path, package['arguments'])
        else:
            os.chdir(package['directory'])
            command = 'python {} {}'.format(package['executor'], package['arguments'])
        print('[  {}  ]     COMMAND: {}'.format(package_name, command))
        os.system(command)


''' ASSISTANT '''
load()