# Explanations: https://fazlurnucom.wordpress.com/2020/06/23/text-extraction-from-a-table-image-using-pytesseract-and-opencv/


## ------------------------------------------------------------------------------------- ##
##                                   PRE-PROCESSING
## ------------------------------------------------------------------------------------- ##


# from preprocessing import get_grayscale, get_binary, invert_area, draw_text, detect
from ROI_selection import detect_lines, get_ROI
# from cv2 import imread, threshold, cvtColor, rectangle, putText, dilate
import cv2 as cv


import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# import cv2 as cv
from ROI_selection import detect_lines, get_ROI
import numpy as np

# def get_grayscale(image):
#     return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

# def get_binary(image):
#     (thresh, blackAndWhiteImage) = cv.threshold(image, 100, 255, cv.THRESH_BINARY)
#     return blackAndWhiteImage

def invert_area(image, x, y, w, h):
    ones = np.copy(image)
    ones = 1
    
    image[ y:y+h , x:x+w ] = ones*255 - image[ y:y+h , x:x+w ] 

    cv.imwrite('inverted.png', image)
    
    # if (display): 
    #     cv.imshow("inverted", image)
    #     cv.waitKey(0)
    #     cv.destroyAllWindows()
    return image
    
def detect(cropped_frame, is_number = False):
    if (is_number):
        text = pytesseract.image_to_string(cropped_frame, config ='-c tessedit_char_whitelist=0123456789 --psm 10 --oem 2')
        # text = pytesseract.image_to_string(cropped_frame, config = '--oem 1') # '-c tessedit_char_whitelist=0123456789 --psm 10 --oem 2')
    else:
        text = pytesseract.image_to_string(cropped_frame, config='--psm 10')
        # text = pytesseract.image_to_string(cropped_frame, config='--oem 1') #'--psm 10')        
        
    return text

def draw_text(src, x, y, w, h, text):
    cFrame = np.copy(src)
    cv.rectangle(cFrame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv.putText(cFrame, "text: " + text, (50, 50), cv.FONT_HERSHEY_SIMPLEX,  
               2, (0, 0, 0), 5, cv.LINE_AA)
    
    return cFrame
        
def erode(img, kernel_size = 5):
    kernel = np.ones((kernel_size,kernel_size), np.uint8) 
    img_erosion = cv.dilate(img, kernel, iterations=2)
    return img_erosion




## ------------------------------------------------------------------------------------- ##
##                                        MAIN
## ------------------------------------------------------------------------------------- ##




def main(display = False, print_text = False, write = False):
    # "D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/CV_Tesseract/Text-Extraction/working_time_testimg/new_edited.jpg"
    filename = 'mark.jpg' # 'new_edited.jpg'
    
    src = cv.imread(filename)
    # src = cv.imread(cv.samples.findFile(filename))
    
    horizontal, vertical = detect_lines(src, minLinLength=350, display=True, write = True)
    print('Horizontal:\n',horizontal, '\n', len(horizontal))
    print('Vertical:\n',vertical, '\n' ,len(vertical))

    ## invert area
    left_line_index = 7
    right_line_index = 13 # 7
    top_line_index = 0
    bottom_line_index = -1
    
    cropped_image, (x, y, w, h) = get_ROI(src, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index)
    
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    cv.imwrite("gray.png", gray)
    bw = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1] # breakpoint here ..............................................
    # cv.imshow("bw", bw)
    cv.imwrite("bw.png", bw)
    bw = invert_area(bw, x, y, w, h)
    cv.imwrite("bw_inver.png", bw)
    #bw = erode(bw, kernel_size=2)
    
    # cv.waitKey(0)
    
    ## set keywords
    keywords = ['1a', '1b', '1c', '2a', '2b', '2c', '3a', '3b', '3c', '4a', '4b', '4c', '5a', '5b', '5c', '6a', '6b', '6c', '7a', '7b', '7c', '8a', '8b', '8c', '9a', '9b', '9c', '10a', '10b', '10c', '11a', '11b', '11c', '12a', '12b', '12c']

    # keywords = ['Order date','Region','Rep','Item','Units','Unit cost','Total']

    # keywords = ['Roll No','Name','1a','2a','3a','4a','5a','6a','7a','8a','9a','10a','11a','12a']
    # 'Roll No','Name','1a','2a','3a','4a','5a','6a','7a','8a','9a','10a','11a','12a',
    # 'Roll No','Name','1a', '1b', '1c', '2a', '2b', '2c', '3a', '3b', '3c', '4a', '4b', '4c', '5a', '5b', '5c', '6a', '6b', '6c', '7a', '7b', '7c', '8a', '8b', '8c', '9a', '9b', '9c', '10a', '10b', '10c', '11a', '11b', '11c', '12a', '12b', '12c'   

    mark_dict = {keyword: [] for keyword in keywords} # giving keyword from keywords list as 'key' & empty list as 'value' for dict 

    ## set counter for image indexing
    counter = 0
    
    ## set line index
    first_line_index = 0
    last_line_index = 13 # 4 - for three row recognition as real ans sheet
    
    ## read text
    print("Text detection started. Please Wait...")
    for i in range(first_line_index, last_line_index):
        for j, keyword in enumerate(keywords):
            counter += 1
            
            # progress = counter/((last_line_index-first_line_index)*len(keywords)) * 100
            # percentage = "%.2f" % progress
            # print("Progress: " + percentage + "%")
            
            left_line_index = j
            right_line_index = j+1
            top_line_index = i
            bottom_line_index = i+1
            
            cropped_image, (x,y,w,h) = get_ROI(bw, horizontal, vertical, left_line_index,
                         right_line_index, top_line_index, bottom_line_index)
            


            if (keywords[j]=='1a'): # Order date
                text = detect(cropped_image)
                print(text) # ------------------------ del at last --------------------------------------
                mark_dict[keyword].append(text)
                
                if (print_text):
                    print("Not number" + ", Row: ", str(i), ", Keyword: " + keyword + ", Text: ", text)
            else:
                text = detect(cropped_image, is_number=True)
                print(text) # ------------------------ del at last --------------------------------------
                mark_dict[keyword].append(text)
                
                if (print_text):
                    print("Is number" + ", Row: ", str(i), ", Keyword: " + keyword + ", Text: ", text)
            
            if (display or write):
                    image_with_text = draw_text(src, x, y, w, h, text)
                    
            # if (display):
                # cv.imshow("detect", image_with_text)
                # cv.waitKey(0)
                # cv.destroyAllWindows()

            if (write):
                cv.imwrite("../Images/"+ str(counter) + ".png", image_with_text)
            
    
    # print(mark_dict)

    import pandas as pd
    df = pd.DataFrame.from_dict(mark_dict)
    new_df = df.replace('\n','', regex=True)

    print(new_df)

    new_df.to_csv('tester.csv', index=False)

    return 0
    
if __name__ == "__main__":
    import time
    st = time.time()
    main()
    print("Time taken: ", round(time.time() - st, 3), "seconds")