import time
st = time.time()

from img2table.document import Image
from img2table.ocr import PaddleOCR
import pandas as pd
import numpy as np
import cv2
import io
from pdf2image import convert_from_path

from PIL import Image as PIL_Image, ImageDraw

# Dictionary for storing marks of each papers
my_dict = {'1a': [], '1b': [], '1c': [], '2a': [], '2b': [], '2c': [], '3a': [], '3b': [], '3c': [], '4a': [], '4b': [], '4c': [], '5a': [], '5b': [], '5c': [], '6a': [], '6b': [], '6c': [], '7a': [], '7b': [], '7c': [], '8a': [], '8b': [], '8c': [], '9a': [], '9b': [], '9c': [], '10a': [], '10b': [], '10c': [], '11a': [], '11b': [], '11c': [], '12a': [], '12b': [], '12c': []}

images = convert_from_path('D:/AJAYMON/AJAY/Programming/S6_Mini_Project/Codes/image to table/Jacob sir COA S4.pdf') # change or give PDF name here....................new_exm.pdf

for i in range(len(images)):
    img = images[i]
    _, height = img.size
    cropped_img = img.crop((150, height / 2 + 50, 1600, height - 300)) # left, top, right, bottom
    # cropped_img.save(f"D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/image to table/temp/ima{i}.jpg") # To save cropped image
    
    img_bytes=io.BytesIO()
    cropped_img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    ## Image opening & performing OCR
    paddle_ocr = PaddleOCR(lang="en")

    doc = Image(img_bytes, dpi=200)
    extracted_tables = doc.extract_tables(ocr=paddle_ocr, implicit_rows=True, min_confidence=50)

    # Load the image using PIL
    img = PIL_Image.open(img_bytes) # comment this --------------------------------------------------

    # Create a draw object
    draw = ImageDraw.Draw(img) # comment this --------------------------------------------------

    for table in extracted_tables:
        for row in table.content.values():
            for cell in row:
                draw.rectangle((cell.bbox.x1, cell.bbox.y1, cell.bbox.x2, cell.bbox.y2), outline="red", width=3)
                
    # img.save(f"D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/image to table/temp/img{i}_with_redlines{i}.jpg") # comment this --------------------------------------------------

    df = table.df
    df = df.iloc[1:, 1:] # deleting first row and column
    df = df.drop(index=df.index[-1]) # remove the last row

    ## Flattening & adding marks to my_dict
    arr = df.to_numpy()
    flat = arr.flatten(order='F') # flattening column-wise
    cell_vals = [i for i in flat]

    print(len(cell_vals)) # comment this --------------------------------------------------

    # Adding values to dictionary
    i = 0
    for key in my_dict:
        my_dict[key].append(cell_vals[i])
        i+=1

## Dictionary to dataframe & it's preprocessing

dict_df = pd.DataFrame(my_dict)

# dict_df.to_csv("D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/image to table/unprocessed_dict.csv", index=False)


# col_name = dict_df.columns[(dict_df == 'None').all()] # finding the column with "None" word
# dict_df = dict_df.drop(col_name, axis=1) # delete the identified columns
# dict_df = dict_df.replace(to_replace="None", value=np.nan) # Replacing all "None" to NaN, which will be empty when converted to CSV
# valid_cols = dict_df.select_dtypes(include=np.number).columns # Select only the valid columns with numeric data types
# dict_df = dict_df.assign(sum=dict_df[valid_cols].sum(axis=1)) # create a new column "row_sum" with the sum of each row
# dict_df = dict_df.assign(Sum_more_than_50=dict_df.apply(lambda x: 'Error' if x['sum'] > 50 else '', axis=1)) # add a new column "error" with "Error" if row_sum is greater than 50

dict_df = dict_df.dropna(axis=1, how='all')

print(dict_df)


# saving dict as csv
dict_df.to_csv("D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/image to table/jacob_sir.csv", index=False)

print(time.time() - st)