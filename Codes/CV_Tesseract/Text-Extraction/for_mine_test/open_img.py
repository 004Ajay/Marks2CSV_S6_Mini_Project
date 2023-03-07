# import cv2
# import glob

# path = "D:\AJAYMON\AJAY\Programming\Auto_Excel_Mark_Entry\Codes\CV_Tesseract\Text-Extraction-Table-Image_workOnThis\images" # change the extension to match the images you have in the folder
# files = glob.glob(path)

# for file in files:
#     img = cv2.imread(file)
#     # ima = cv2.resize(img, (700,750), interpolation = cv2.INTER_AREA)
#     cv2.imshow(file, img)
#     cv2.waitKey(0)

# cv2.destroyAllWindows()

import cv2
import os

folder = "D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/CV_Tesseract/Text-Extraction-Table-Image_workOnThis/test_images"

images = []
for filename in os.listdir(folder):
    img = cv2.imread(os.path.join(folder,filename))
    ima = cv2.resize(img, (650,750), interpolation = cv2.INTER_AREA)
    cv2.imshow('file',ima)
    cv2.waitKey(0)

cv2.destroyAllWindows()   