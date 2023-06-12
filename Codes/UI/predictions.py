import pandas as pd
import tensorflow as tf
from img2table.document import Image
from diffCellFns import classify_image,cell_extraction_classification_df_return,dataframe_postprocessing
import io
from PIL import Image as PIL_Image, ImageDraw

def return_dictonary(imgs,model):
    # Dictionary for storing marks of each papers
    my_dict = {'1a': [], '1b': [], '1c': [], '2a': [], '2b': [], '2c': [], '3a': [], '3b': [], '3c': [], '4a': [], '4b': [], '4c': [], '5a': [], '5b': [], '5c': [], '6a': [], '6b': [], '6c': [], '7a': [], '7b': [], '7c': [], '8a': [], '8b': [], '8c': [], '9a': [], '9b': [], '9c': [], '10a': [], '10b': [], '10c': [], '11a': [], '11b': [], '11c': [], '12a': [], '12b': [], '12c': []}    
    
    for i in range(len(imgs)):
        img = imgs[i]
        dpi=(200,200)
        img.info["dpi"]=dpi
        img_bytes=io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        doc = Image(img_bytes)
        extracted_tables = doc.extract_tables(implicit_rows=False, min_confidence=50)
        orddict = extracted_tables[0].content
        img=PIL_Image.open(img_bytes)
        if len(orddict.keys()) == 5 and sum(len(value) for value in orddict.values())== 65:# if the table recognition is correct, the no of rows will be 5
            paper_df = cell_extraction_classification_df_return(orddict,img,model)
            marks_for_main_dict = dataframe_postprocessing(paper_df)

            for key, value in zip(my_dict.keys(), marks_for_main_dict):
                my_dict[key].append(value) # Adding values to dictionary

        else: # if the table recognition is incorrect
            for key in my_dict.keys():
                my_dict[key].append(0) # Adding values to dictionary
    return my_dict