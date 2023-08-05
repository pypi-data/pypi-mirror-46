from microlab import Files
import os


print('TEST JSON \n')
dummy_filename = 'test.json'
folder_path = os.getcwd()
filename = os.path.join(folder_path, dummy_filename)

# Data
data = {'name': 'Test', 'id': 10}

#  Create
Files.create_json(data=data, path=filename, verbose=True)

#  Read
data = Files.read_json(path=filename, verbose=True)

# Update
new_data = {'name': 'new name'}
Files.update_file(data=new_data, path=filename, verbose=True)

# Delete
Files.delete_file(path=filename, verbose=True)

