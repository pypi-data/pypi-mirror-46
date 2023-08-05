import json
import os
import shutil

""" UPDATE """
def update_file(data, path, verbose=False):
    if verbose:
        print('[  U  ]  {}'.format(path), end='.....')
    if os.path.isfile(path):
        old_data = read_json(path=path,verbose=False)
        old_data.update(data)
        create_json(data=old_data, path=path, verbose=False)
        print('[ OK ] replace the old json')
    else:
        print('[ !! ] file not found')

""" DELETE """
def delete_file(path, verbose=False):

    print('[  D  ]  {}'.format(path), end='.....')

    if os.path.isfile(path):
        os.remove(path)
        if verbose:
            print('[ OK ] delete the file json')
    else:
        print('[ !! ] file not found')

""" JSON """
def read_json(path, verbose=False):
    if verbose:
        print('[  R  ]  {}'.format(path), end='.....')
    # file exist
    if os.path.isfile(path):
        with open(path, 'r') as f:
            data = json.load(f)
        if verbose:
            print('[ OK ] load from exist json')
        return data
    # file not exist
    else:
        if verbose:
            print('[ !! ] file not found ')
        return {}


def create_json(data, path, verbose=False):
    if verbose:
        print('[  C  ]  {}'.format(path), end='.....')
    # file exists
    if os.path.isfile(path):
        if verbose:
            print('[ OK ] replace the old json')

    # file not exists
    else:
        if verbose:
            print('[ OK ] create new file json')
    with open(path, 'w') as f:
        f.write(json.dumps(data))

