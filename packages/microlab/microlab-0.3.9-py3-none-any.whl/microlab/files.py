import json
import os
import shutil
import patoolib
import zipfile

dir = os.getcwd()


""" FOLDERS """
def folder_exist(path, verbose=False):
    if os.path.isdir(path):
        return True
    else:
        if verbose:
            print('[ !! ] folder not found')
        return False
def create_folder(path, verbose=False):
    if verbose:
        print('[  C  ]  {}'.format(path), end='.....')
    # folder exists
    if folder_exist(path=path, verbose=False):
        if verbose:
            print('[ OK ] folder exists')

    # folder not exists
    else:
        if verbose:
            print('[ OK ] create new folder')
        os.mkdir(path=path)
def delete_folder(path, verbose=False):
    if verbose:
        print('[  D  ]  {}'.format(path), end='.....')
    if folder_exist(path=path, verbose=False):
        shutil.rmtree(path=path)
        if verbose:
            print('[ OK ] delete the folder')


""" FILES """
def file_exist(path, verbose=False):
    if os.path.isfile(path):
        return True
    else:
        if verbose:
            print('[ !! ] filenot found')
        return False
def create_file(path,data, verbose=False):
    if verbose:
        print('[  C  ]  {}'.format(path), end='.....')
    if type(data) == str:
        string = data
    elif type(data) == bytes:
        string = data.decode('utf-8')
    # wite data to dile
    with open(path, mode='w', encoding='utf-8') as f:
        f.write(string)
    if verbose:
        print('[ OK ] create file')
def read_file(path, verbose=False):
    if verbose:
        print('[  R  ]  {}'.format(path), end='.....')
    data = ''
    if file_exist(path=path, verbose=False):
        with open(path, 'r') as f:
            data = f.read()
        print('[ OK ] read file')
    return data
def update_file(path, data, verbose=False):
    if verbose:
        print('[  U  ]  {}'.format(path), end='.....')
    if file_exist(path=path, verbose=False):
        create_file(path=path, data=data, verbose=False)
        if verbose:
            print('[ OK ] update file')
def delete_file(path, verbose=False):
    print('[  D  ]  {}'.format(path), end='.....')
    if file_exist(path=path, verbose=verbose):
        os.remove(path)
        if verbose:
            print('[ OK ] delete  file')


""" JSON """
def create_json(data, path, verbose=False):
    if verbose:
        print('[  C  ]  {}'.format(path), end='.....')
    # file exists
    if file_exist(path=path, verbose=False):
        if verbose:
            print('[ OK ] replace the old json')

    # file not exists
    else:
        if verbose:
            print('[ OK ] create new file json')

    with open(path, 'w') as f:
        f.write(json.dumps(data))
def read_json(path, verbose=False):
    if verbose:
        print('[  R  ]  {}'.format(path), end='.....')
    if file_exist(path=path, verbose=verbose):
        with open(path, 'r') as f:
            data = json.load(f)
        if verbose:
            print('[ OK ] load from exist json')
        return data
    else:
        return {}
def update_json(data, path, verbose=False):
    if verbose:
        print('[  U  ]  {}'.format(path), end='.....')
    if file_exist(path=path, verbose=False):
        old_data = read_json(path=path, verbose=False)
        old_data.update(data)
        create_json(data=old_data, path=path, verbose=False)
        print('[ OK ] replace the old json')


""" ZIP """
def create_zip(source, destination, verbose=False):
    # cd to Repos directory
    parrent_folder = '\\'.join(source.split('/')[:-1])
    # input(parrent_folder)
    # os.chdir(parrent_folder)

    # zip_file = '{}.zip'.format(source)

    # if zip found, delete it
    if file_exist(path=destination, verbose=False):
        os.remove(destination)

    # create zip file
    if verbose:
        print('creating zip for {}'.format(source))
    patoolib.create_archive(destination, (source,), verbosity=-1)

    # cd back to root
    os.chdir(dir)

    # move the zip from repos to zips
    zip_file_in_repos = ''.format(destination)
    # zip_file_in_zips = 'Zips/{}.zip'.format(path)
    # shutil.move(zip_file_in_repos, zip_file_in_zips)
    if verbose:
        print('{} created'.format(destination))
def extract_zip(source, destination, verbose=False):
    if verbose:
        print('[  E  ]  {}'.format(destination), end='.....')
    if file_exist(path=source, verbose=verbose):
        zip_ref = zipfile.ZipFile(source, 'r')
        zip_ref.extractall(destination)
        zip_ref.close()
        if verbose:
            print('[ OK ] zip  extracted ')


""" CSV """


""" XLS """


""" YAML """
