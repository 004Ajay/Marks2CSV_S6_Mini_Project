import pandas as pd
import numpy as np
import pytesseract
import requests, time, math, cv2, os

st = time.time() # start time

def read_image(img_src):
    img_data = requests.get(img_src).content
    with open('pass.png', 'wb') as handler:
        handler.write(img_data)

    img = cv2.imread('pass.png',0)
    (height, width) = img.shape

    os.remove("pass.png")

    return img, height, width

def image_preprocess(img): # Canny - detect edges, HoughLines - map out the shape of our passport area
    img_canny = cv2.Canny(img, 50, 100, apertureSize = 3)
    img_hough = cv2.HoughLinesP(img_canny, 1, math.pi / 180, 100, minLineLength = 100, maxLineGap = 10)

    (x, y, w, h) = (np.amin(img_hough, axis = 0)[0,0], np.amin(img_hough, axis = 0)[0,1],
    np.amax(img_hough, axis = 0)[0,0] - np.amin(img_hough, axis = 0)[0,0],
    np.amax(img_hough, axis = 0)[0,1] - np.amin(img_hough, axis = 0)[0,1]) # defining x, y, w, h

    img_roi = img[y:y+h,x:x+w]

    return img_roi

def mrz_selection(img_roi): # mrz - machine readable zone
    (height, width) = img_roi.shape
    dim_mrz = (1, round(height*0.9), width-3, round(height-(height*0.9)))
    
    return dim_mrz

def mrz_postprocess(mrz):
    mrz = [line for line in mrz.split('\n') if len(line)>10]
    if mrz[0][0:2] == 'P<':
        lastname = mrz[0].split('<')[1][3:]
    else:
        lastname = mrz[0].split('<')[0][5:]
    
    firstname = [i for i in mrz[0].split('<') if (i).isspace() == 0 and len(i) > 0][1]
    pp_no = mrz[1][:9]

    return lastname, firstname, pp_no

def ocr_on_selection(dim, img_roi, config, lang = None):
    
    (x, y, w, h) = dim
    img_roi = cv2.rectangle(img_roi, (x, y), (x + w ,y + h),(0,0,0))
    img_select = img_roi[y:y+h, x:x+w]

    # cv2.imwrite('image.jpg', img_select)

    img_select =cv2.GaussianBlur(img_select, (3,3), 0)
    ret, img_select = cv2.threshold(img_select,127,255,cv2.THRESH_TOZERO)
    output_str = pytesseract.image_to_string(img_select, lang, config)

    return output_str

# Tesseract-OCR installation location
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe" # add the pytesseract location of your PC

img_src = 'https://upload.wikimedia.org/wikipedia/commons/a/a6/People%27s_Republic_of_China_Passport_%2897-2_version_for_Single_Exit_and_Entry%29.png' # test using normal image
img, height, width = read_image(img_src)

img_roi = image_preprocess(img)

img_mrz = mrz_selection(img_roi)

dim_mrz = mrz_selection(img_roi)

mrz = ocr_on_selection(dim_mrz, img_roi, '--psm 12')
lastname, firstname, pp_no = mrz_postprocess(mrz)

dim_lastname_chi = (140, 305, 45, 25)
dim_firstname_chi = (140, 335, 45, 25)

lastname_chi = ocr_on_selection(dim_lastname_chi, img_roi, '--psm 7', lang = 'chi_sim')
lastname_chi_splitted = lastname_chi.split('\n')[0]

firstname_chi = ocr_on_selection(dim_firstname_chi, img_roi, '--psm 7', lang = 'chi_sim')
firstname_chi_splitted = firstname_chi.split('\n')[0]

passport_dict = {'Passport No.': pp_no,
                 'First Name': firstname,
                 'Last Name': lastname,
                 'First Name_chi (汉字)': firstname_chi_splitted,
                 'Last Name_chi (汉字)': lastname_chi_splitted}

output = pd.DataFrame(columns = ['Passport No.','First Name','Last Name','First Name_chi (汉字)','Last Name_chi (汉字)'])
temp_df = pd.DataFrame.from_dict(passport_dict,orient='index').T
output = pd.concat([output,temp_df])
# output.to_csv('test.csv')
print(output)
# print(time.time() -  st) # end time & print total time