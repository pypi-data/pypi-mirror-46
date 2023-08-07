from microlab.cryptography.symmetric import SymmetricCryptography
from microlab.io.folders import create_folder, delete_folder
from microlab.io.files import create_file, delete_file

import os

# Workspace directories
original_folder = os.path.join(os.getcwd(), 'original')
encrypted_folder = os.path.join(os.getcwd(), 'encrypted')
decrypted_folder = os.path.join(os.getcwd(), 'decrypted')
keys_folder = os.path.join(os.getcwd(), 'keys')

# Original data
data_file = os.path.join(original_folder, 'data.txt')
data = 'hello wold'

if __name__ == '__main__':
    print('\n ~ TEST SYMMETRIC CRYPTOGRAPHY')

    # Create folders                                              This will be inside of the SymmetricCryptography class
    create_folder(path=original_folder, verbose=True)
    create_folder(path=encrypted_folder, verbose=True)
    create_folder(path=decrypted_folder, verbose=True)
    create_folder(path=keys_folder, verbose=True)

    # Create data in original
    create_file(path=data_file, data=data, verbose=True)

    #  Initialize cryptography
    obj = SymmetricCryptography(originals_folder=original_folder,
                                encrypted_folder=encrypted_folder,
                                decrypted_folder=decrypted_folder,
                                keys_folder=keys_folder)

    # Generate a key
    obj.generate_key(key_name='test_key')

    # Encrypt the data using the key
    obj.encrypt_file(original_file_name='data.txt', key_name='test_key')
    delete_file(path=data_file,verbose=True)
    # Decrypt the data using the key
    obj.decrypt_file(encrypted_file_name='data.txt', key_name='test_key')

    # Get the output data
    decrypted = obj.read_decrypted(file_name='data.txt')

    # Delete folders
    delete_folder(path=original_folder, verbose=True)
    delete_folder(path=encrypted_folder, verbose=True)
    delete_folder(path=decrypted_folder, verbose=True)
    delete_folder(path=keys_folder, verbose=True)

    # Validate the output data based on original data
    if decrypted == data:
        print('[ OK  ]  data integrity is approved ')
    else:
        print('[ !!  ] data integrity is unqualified ')
