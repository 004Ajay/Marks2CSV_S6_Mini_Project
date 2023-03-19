from PIL import Image
import os

input_folder = 'path/to/input/folder'
output_folder = 'path/to/output/folder'

# Define the size to which images should be resized
new_size = (500, 500)

# Loop through all the files in the input folder
for file_name in os.listdir(input_folder):
    # Check if the file is an image (you may want to modify this depending on the types of files in your folder)
    if file_name.endswith('.jpg') or file_name.endswith('.png'):
        # Open the image
        image = Image.open(os.path.join(input_folder, file_name))
        # Resize the image
        resized_image = image.resize(new_size)
        # Save the resized image to the output folder with the same file name
        resized_image.save(os.path.join(output_folder, file_name))
