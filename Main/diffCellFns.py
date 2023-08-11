import numpy as np
import cv2
import pandas as pd

def classify_image(image,model):
    """
    Classify the image to numbers from 0 to 8, 8 is None
    
    Parameter
    ---------
    image: ndarray of a single channel image.
    
    Return
    ------
    pred: classified value corresponding to input image
    
    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    resized = cv2.resize(gray, (40, 40)) # 40x40 pixels is the input shape of model

    # Expand the dimensions of the image to match the input shape of the model
    im = np.expand_dims(resized, axis=0)

    result = model.predict(im)
    pred = np.argmax(result[0])

    return pred

def cell_extraction_classification_df_return(orddict,img,model):
    """
    Extracts cells of the image from the bbox values in orddict,
    classify the image using our custom ocr model, and returns the result as a dataframe
    
    Parameter
    ---------
    orddict: ordered Dictionary having 4 values of bbox
    
    Return
    ------
    df: dataframe of classified values
    
    """
    del orddict[0], orddict[4] # del the first and last keys (rows) of orddict
    pred = []
    for key, cell_list in orddict.items(): # do the bbox extrn and classification using our model
        for cell in cell_list:
            x1 = cell.bbox.x1
            y1 = cell.bbox.y1
            x2 = cell.bbox.x2
            y2 = cell.bbox.y2

            new_im = img.crop((x1, y1, x2, y2))
            im_arr = np.array(new_im) # Converting new_im (PIL.Image.Image) to numpy array for predict_image()
            pred.append(classify_image(im_arr,model))
    pred = [0 if num == 8 else num for num in pred]
    pred_arr = np.array(pred)
    reshaped_pred_arr = pred_arr.reshape(3, 13) # 3 rows and 13 columns
    df = pd.DataFrame(reshaped_pred_arr)
    return df

def dataframe_postprocessing(paper_df):
    """
    Preprocessing the dataframe - removing first column,
    flattening the np.array of df column-wise,
    and returns the values to be added to main mark-dictionary
        
    Parameter
    ---------
    paper_df: Output of cell_extraction_classification_df_return(), df with the unwanted first column
    
    Return
    ------
    cell_vals: Values to be added to main mark-dictionary
    
    """
    paper_df = paper_df.iloc[: , 1:] # iloc[row, column], removing first column

    # Flattening & adding marks to my_dict
    paper_arr = paper_df.to_numpy()
    flat = paper_arr.flatten(order='F') # F - flattening column-wise
    cell_vals = [i for i in flat]

    return cell_vals

