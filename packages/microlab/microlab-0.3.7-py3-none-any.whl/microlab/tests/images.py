from microlab import Images
from microlab.Files import delete_file
import os

dir = os.getcwd()

# image Data
filename = os.path.join(dir, '4.jpg')
img = Images.read_image(path=filename, verbose=True)

# Create image
Images.create_image(path=filename, image=img, verbose=True)

# Read image
image = Images.read_image(path=filename, verbose=True)

# Update image
Images.update_image(path=filename, image=image, verbose=True)

# Delete image
# delete_file(path=filename, verbose=True)