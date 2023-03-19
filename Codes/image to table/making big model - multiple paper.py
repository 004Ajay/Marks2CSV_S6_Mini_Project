import time
st = time.time()

from img2table.document import Image
from img2table.ocr import PaddleOCR
import pandas as pd
import numpy as np
import cv2
from pdf2image import convert_from_path

from PIL import Image as PIL_Image, ImageDraw

# Dictionary for storing marks of each papers
my_dict = {'1a': [], '1b': [], '1c': [], '2a': [], '2b': [], '2c': [], '3a': [], '3b': [], '3c': [], '4a': [], '4b': [], '4c': [], '5a': [], '5b': [], '5c': [], '6a': [], '6b': [], '6c': [], '7a': [], '7b': [], '7c': [], '8a': [], '8b': [], '8c': [], '9a': [], '9b': [], '9c': [], '10a': [], '10b': [], '10c': [], '11a': [], '11b': [], '11c': [], '12a': [], '12b': [], '12c': []}

images = convert_from_path('D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/image to table/new_exm.pdf') # change or give PDF name here....................

for i in range(len(images)):
    img = images[i]
    _, height = img.size
    cropped_img = img.crop((150, height / 2 + 50, 1600, height - 300)) # left, top, right, bottom
    # cropped_img.save(f"D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/image to table/temp/ima{i}.jpg")
    
    img = np.array(cropped_img)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # # Apply thresholding to make the black lines more black and white areas more white
    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # # Apply morphological operations to further enhance the image
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # # Apply dilation to make the lines thicker
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    # dilated = cv2.dilate(closed, kernel, iterations=1)
    
    cv2.imwrite(f"D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/image to table/temp/ima{i}.jpg", gray)

# ----------------------------------------------------------------------------------------------------------------------------------    

for i in range(len(images)):
    ## Image opening & performing OCR
    paddle_ocr = PaddleOCR(lang="en")
    src = f"D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/image to table/temp/ima{i}.jpg"

    doc = Image(src, dpi=200)
    extracted_tables = doc.extract_tables(ocr=paddle_ocr, implicit_rows=True, min_confidence=50)

    # Load the image using PIL
    img = PIL_Image.open(src) # comment this --------------------------------------------------

    # Create a draw object
    draw = ImageDraw.Draw(img) # comment this --------------------------------------------------

    for table in extracted_tables:
        for row in table.content.values():
            for cell in row:
                draw.rectangle((cell.bbox.x1, cell.bbox.y1, cell.bbox.x2, cell.bbox.y2), outline="red", width=3)
                
    img.save(f"D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/image to table/temp/img{i}_with_redlines{i}.jpg") # comment this --------------------------------------------------

    df = table.df
    df = df.iloc[1:, 1:] # deleting first row and column
    df = df.drop(index=df.index[-1]) # remove the last row

    ## Flattening & adding marks to my_dict
    arr = df.to_numpy()
    flat = arr.flatten(order='F') # flattening column-wise
    cell_vals = [str(i) for i in flat]

    print(len(cell_vals)) # comment this --------------------------------------------------

    # Adding values to dictionary
    i = 0
    for key in my_dict:
        my_dict[key].append(cell_vals[i])
        i+=1

## Dictionary to dataframe & it's preprocessing
### The df output may have 'None' values but they're actually NaN, so they won't come in exported CSV file
dict_df = pd.DataFrame(my_dict)
dict_df = dict_df.dropna(axis=1, how='all')

# col_name = dict_df.columns[(dict_df == 'None').all()] # finding the column with "None" word
# dict_df = dict_df.drop(col_name, axis=1) # delete the identified columns
# dict_df = dict_df.replace(to_replace="None", value=np.nan) # Replacing all "None" to NaN, which will be empty when converted to CSV

dict_df.to_csv("D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/image to table/big_model_dict.csv", index=False) # saving dict as csv

print("Total time taken: ", time.time() - st)