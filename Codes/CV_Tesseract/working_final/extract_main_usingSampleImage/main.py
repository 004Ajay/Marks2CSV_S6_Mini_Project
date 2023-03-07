# Explanations: https://fazlurnucom.wordpress.com/2020/06/23/text-extraction-from-a-table-image-using-pytesseract-and-opencv/


## ------------------------------------------------------------------------------------- ##
##                                   ROI_SELECTION                                       ##
## ------------------------------------------------------------------------------------- ##

from cv2 import (imread, threshold, cvtColor, rectangle, putText, dilate,
                 FONT_HERSHEY_SIMPLEX, COLOR_BGR2GRAY, THRESH_BINARY_INV, THRESH_OTSU, LINE_AA,
                 HoughLinesP, Canny, imwrite, imshow, waitKey, destroyAllWindows)
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

def is_vertical(line):
    return line[0]==line[2]

def is_horizontal(line):
    return line[1]==line[3]
    
def overlapping_filter(lines, sorting_index):
    filtered_lines = []
    
    lines = sorted(lines, key=lambda lines: lines[sorting_index])
    
    for i in range(len(lines)):
            l_curr = lines[i]
            if(i>0):
                l_prev = lines[i-1]
                if ( (l_curr[sorting_index] - l_prev[sorting_index]) > 5):
                    filtered_lines.append(l_curr)
            else:
                filtered_lines.append(l_curr)
                
    return filtered_lines
               
def detect_lines(image, title='default', rho = 1, theta = np.pi/180, threshold = 50, minLinLength = 290, maxLineGap = 6, display = False, write = False):

    gray = cvtColor(image, COLOR_BGR2GRAY)
    if gray is None:
        print ('Error opening image!')
        return -1
    
    dst = Canny(gray, 50, 150, None, 3)
    
    # Copy edges to the images that will display the results in BGR
    cImage = np.copy(image)
    
    #linesP = HoughLinesP(dst, 1 , np.pi / 180, 50, None, 290, 6)
    linesP = HoughLinesP(dst, rho , theta, threshold, None, minLinLength, maxLineGap)
    
    horizontal_lines = []
    vertical_lines = []
    
    if linesP is not None:
        #for i in range(40, nb_lines):
        for i in range(0, len(linesP)):
            l = linesP[i][0]

            if (is_vertical(l)):
                vertical_lines.append(l)
                
            elif (is_horizontal(l)):
                horizontal_lines.append(l)
        
        horizontal_lines = overlapping_filter(horizontal_lines, 1)
        vertical_lines = overlapping_filter(vertical_lines, 0)
            
    # if (display):
    #     for i, line in enumerate(horizontal_lines):
    #         line(cImage, (line[0], line[1]), (line[2], line[3]), (0,255,0), 3, LINE_AA)
            
    #         putText(cImage, str(i) + "h", (line[0] + 5, line[1]), FONT_HERSHEY_SIMPLEX,  
    #                    0.5, (0, 0, 0), 1, LINE_AA) 
            
    #     for i, line in enumerate(vertical_lines):
    #         line(cImage, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, LINE_AA)
    #         putText(cImage, str(i) + "v", (line[0], line[1] + 5), FONT_HERSHEY_SIMPLEX,  
    #                    0.5, (0, 0, 0), 1, LINE_AA) 
            
        imshow("Source", cImage)
        #imshow("Canny", cdstP)
        # waitKey(0)
        # destroyAllWindows()
        
    # if (write):
    #     imwrite(f"{title}.png", cImage)
        
    return (horizontal_lines, vertical_lines)
    
def get_ROI(image, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index, offset=4):
    x1 = vertical[left_line_index][2] + offset
    y1 = horizontal[top_line_index][3] + offset
    x2 = vertical[right_line_index][2] - offset
    y2 = horizontal[bottom_line_index][3] - offset
    
    w = x2 - x1
    h = y2 - y1
    
    cropped_image = image[ y1:y1+h , x1:x1+w ]
    # imshow('crop', cropped_image)
    # waitKey(0)
    
    return cropped_image, (x1, y1, w, h)

# def main(argv):
    
#     default_file = 'images/source6.png'
#     filename = argv[0] if len(argv) > 0 else default_file
    
#     src = imread(samples.findFile(filename))
    
#     # Loads an image
#     horizontal, vertical = detect_lines(src, display=True)
    
#     return 0
    
# if __name__ == "__main__":
#     main(sys.argv[1:])



## ------------------------------------------------------------------------------------- ##
##                                   PRE-PROCESSING                                      ##
## ------------------------------------------------------------------------------------- ##


def invert_area(image, x, y, w, h):
    ones = np.copy(image)
    ones = 1
    
    image[ y:y+h , x:x+w ] = ones*255 - image[ y:y+h , x:x+w ] 

    # imwrite('inverted.png', image)
    
    # if (display): 
    #     imshow("inverted", image)
    #     waitKey(0)
    #     destroyAllWindows()
    return image
    
def detect(cropped_frame, is_number = False):
    if (is_number):
        text = pytesseract.image_to_string(cropped_frame, config = '--oem 1') # '-c tessedit_char_whitelist=0123456789 --psm 10 --oem 2')
    else:
        text = pytesseract.image_to_string(cropped_frame, config='--oem 1') #'--psm 10')        
        
    return text

def draw_text(src, x, y, w, h, text):
    cFrame = np.copy(src)
    rectangle(cFrame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    putText(cFrame, "text: " + text, (50, 50), FONT_HERSHEY_SIMPLEX,  
               2, (0, 0, 0), 5, LINE_AA)
    
    return cFrame
        
# def erode(img, kernel_size = 5):
#     kernel = np.ones((kernel_size,kernel_size), np.uint8) 
#     img_erosion = dilate(img, kernel, iterations=2)
#     return img_erosion


## ------------------------------------------------------------------------------------- ##
##                                        MAIN                                           ##
## ------------------------------------------------------------------------------------- ##


def main(display = False, print_text = False, write = False):
    filename = "D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/CV_Tesseract/Text-Extraction/extractor_main/new.jpg" #'new.jpg'
    
    src = imread(filename)
    # src = imread(samples.findFile(filename))
    
    horizontal, vertical = detect_lines(src, minLinLength=350, display=True, write = True)
    # print(horizontal, '\n', len(horizontal))
    # print(vertical, '\n' ,len(vertical))

    ## invert area
    left_line_index = 0
    right_line_index = 7
    top_line_index = 0
    bottom_line_index = -1
    
    cropped_image, (x, y, w, h) = get_ROI(src, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index)
    imshow('cropped', cropped_image)
    waitKey(0)
    gray = cvtColor(src, COLOR_BGR2GRAY)
    imwrite("gray.png", gray) # ------------------------ del at last --------------------------------------
    bw = threshold(gray, 0, 255, THRESH_BINARY_INV + THRESH_OTSU)[1] # breakpoint here ..............................................
    imshow("Black & White", bw) # ------------------------ del at last --------------------------------------
    imwrite("bw.png", bw) # ------------------------ del at last --------------------------------------
    bw = invert_area(bw, x, y, w, h)
    imwrite("bw_inver.png", bw) # ------------------------ del at last --------------------------------------

    #bw = erode(bw, kernel_size=2)

    waitKey(0)
    
    ## Column headers here ................
    keywords = ['Order date','Region','Rep','Item','Units','Unit cost','Total']

    # keywords = ['Name','1a','2a','3a','4a','5a','6a','7a','8a','9a','10a','11a','12a']
    # 'Name','1a','2a','3a','4a','5a','6a','7a','8a','9a','10a','11a','12a',
    # 'Name','1a', '1b', '1c', '2a', '2b', '2c', '3a', '3b', '3c', '4a', '4b', '4c', '5a', '5b', '5c', '6a', '6b', '6c', '7a', '7b', '7c', '8a', '8b', '8c', '9a', '9b', '9c', '10a', '10b', '10c', '11a', '11b', '11c', '12a', '12b', '12c'   

    mark_dict = {}
    for keyword in keywords:
        mark_dict[keyword] = []
        
    ## set counter for image indexing
    counter = 0
    
    ## set line index
    first_line_index = 1
    last_line_index = 9
    
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
            


            if (keywords[j]=='Order date'):
                text = detect(cropped_image)
                # print(text) # ------------------------ del at last --------------------------------------
                mark_dict[keyword].append(text)
                
                if (print_text):
                    print("Not number" + ", Row: ", str(i), ", Keyword: " + keyword + ", Text: ", text)
            else:
                text = detect(cropped_image, is_number=True)
                # print(text) # ------------------------ del at last --------------------------------------
                mark_dict[keyword].append(text)
                
                if (print_text):
                    print("Is number" + ", Row: ", str(i), ", Keyword: " + keyword + ", Text: ", text)
            
            if (display or write):
                    image_with_text = draw_text(src, x, y, w, h, text)
                    
            # if (display):
                # imshow("detect", image_with_text)
                # waitKey(0)
                # destroyAllWindows()

            # if (write):
            #     imwrite("../Images/"+ str(counter) + ".png", image_with_text)
            
    
    # print(mark_dict)

    import pandas as pd
    df = pd.DataFrame.from_dict(mark_dict)
    new_df = df.replace('\n','', regex=True)

    print(new_df)

    new_df.to_csv('tester.csv', index=False)

    return 0
    
if __name__ == "__main__":
    # import time # ------------------------ del at last --------------------------------------
    # st = time.time() # ------------------------ del at last --------------------------------------
    main()
    # print(time.time() - st) # ------------------------ del at last --------------------------------------