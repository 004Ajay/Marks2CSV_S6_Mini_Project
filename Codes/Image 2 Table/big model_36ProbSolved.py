from img2table.document import Image
from img2table.ocr import PaddleOCR
import pandas as pd
from pdf2image import convert_from_path
from PIL import Image as PIL_Image, ImageDraw
import io

# Dictionary for storing marks of each papers
my_dict = {'1a': [], '1b': [], '1c': [], '2a': [], '2b': [], '2c': [], '3a': [], '3b': [], '3c': [], '4a': [], '4b': [], '4c': [], '5a': [], '5b': [], '5c': [], '6a': [], '6b': [], '6c': [], '7a': [], '7b': [], '7c': [], '8a': [], '8b': [], '8c': [], '9a': [], '9b': [], '9c': [], '10a': [], '10b': [], '10c': [], '11a': [], '11b': [], '11c': [], '12a': [], '12b': [], '12c': []}

images = convert_from_path("D:/AJAYMON/AJAY/Programming/S6_Mini_Project/Codes/image to table/MP_pdf2.pdf") # change or give PDF name here
ext_dict = {}
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

    ############## ----------- UNCOMMENT THIS ONLY FOR SAVING TABLE IMAGE WITH RED OUTLINE ----------- ##############


    # # Load the image using PIL
    # img = PIL_Image.open(src) # comment this --------------------------------------------------

    # # Create a draw object
    # draw = ImageDraw.Draw(img) # comment this --------------------------------------------------

    # for table in extracted_tables:
    #     for row in table.content.values():
    #         for cell in row:
    #             draw.rectangle((cell.bbox.x1, cell.bbox.y1, cell.bbox.x2, cell.bbox.y2), outline="red", width=3)
                
    # img.save(f"D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/image to table/temp/img{i}_with_redlines{i}.jpg") # comment this --------------------------------------------------


    ############## ----------- UNCOMMENT THIS ONLY FOR SAVING TABLE IMAGE WITH RED OUTLINE ----------- ##############

    df = extracted_tables[0].df
    df = df.iloc[1:, 1:] # deleting first row and column
    df = df.drop(index=df.index[-1]) # remove the last row

    ## Flattening & adding marks to my_dict
    arr = df.to_numpy()
    flat = arr.flatten(order='F') # flattening column-wise
    
    cell_vals = [0 if item is None else item for item in flat] # Changing all None to 0 in mark cells

    flat_len = len(cell_vals)
    ext_dict[i+1] = flat_len

    print(i+1, "-", flat_len) # comment this --------------------------------------------------

    if flat_len == 36: # 36 is the total number of mark cells,  CHECK THIS ////////////////////////////////////////////////////////////////////////
        for key, value in zip(my_dict.keys(), cell_vals):
            my_dict[key].append(value) # Adding values to dictionary
    else:
        for key in my_dict.keys():
            my_dict[key].append(0) # Adding values to dictionary

print(my_dict)

dict_df = pd.DataFrame(my_dict)

for column in dict_df.columns:
    if len(dict_df[column].unique()) == 1: # column contains the same value (1 value only) from start to end
        dict_df = dict_df.drop(column, axis=1) # Drop the column

# Dictionary to dataframe & it's preprocessing
# import numpy as np

# dict_df = pd.DataFrame(my_dict)

# dict_copy = dict_df

# col_name = dict_df.columns[(dict_df == 'None').all()] # finding the column with "None" word
# dict_df = dict_df.drop(col_name, axis=1) # delete the identified columns
# dict_df = dict_df.replace(to_replace="None", value=np.nan) # Replacing all "None" to NaN, which will be empty when converted to CSV

# valid_cols = dict_df.select_dtypes(include=np.number).columns # Select only the valid columns with numeric data types
# dict_df = dict_df.assign(sum=dict_df[valid_cols].sum(axis=1)) # create a new column "row_sum" with the sum of each row
# dict_df = dict_df.assign(Sum_more_than_50=dict_df.apply(lambda x: 'Error' if x['sum'] > 50 else '', axis=1)) # add a new column "error" with "Error" if row_sum is greater than 50

# dict_df = dict_df.dropna(axis=1, how='all')
# dict_df.fillna(0, inplace=True)

print(ext_dict)

for key, value in ext_dict.items(): # for finding the papers with table detection error
    if value != 36:
        print(key, "-", value)

print(dict_df)        

dict_df.to_csv("D:/AJAYMON/AJAY/Programming/S6_Mini_Project/Codes/image to table/36_cell_from_py_file.csv", index=False)