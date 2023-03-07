import cv2
# import numpy as np
 
if __name__ == '__main__' :
 
    # Read image

    filepath = "D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/CV_Tesseract/Text-Extraction/for_mine_test/hridya.jpg"
    im = cv2.imread(filepath)
    # image = cv2.resize(im, (650,750), interpolation = cv2.INTER_AREA)
    image = cv2.resize(im, (620,877), interpolation = cv2.INTER_AREA)
 
    # Select ROI
    # r = cv2.selectROI(image)
    # print(r)
    # imCrop = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    x,y,w,h = (48, 463, 544, 261) 
    imCroped = image[y:y+h, x:x+w]
    cv2.imshow("Image", imCroped)
    # cv2.imshow("Image", imCrop)

    cv2.waitKey(0)