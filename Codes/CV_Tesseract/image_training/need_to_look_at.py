import cv2
import numpy as np
import os

# Define the input and output directories
input_dir = "input_images"
output_dir = "output_images"

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through all the images in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".jpg"):
        # Load the image
        image = cv2.imread(os.path.join(input_dir, filename))

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Threshold the image to binary
        threshold_value, thresholded = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Dilate the image to fill in gaps
        kernel = np.ones((5,5), np.uint8)
        dilated = cv2.dilate(thresholded, kernel, iterations=1)

        # Save the pre-processed image
        output_filename = os.path.splitext(filename)[0] + "_preprocessed.jpg"
        cv2.imwrite(os.path.join(output_dir, output_filename), dilated)
