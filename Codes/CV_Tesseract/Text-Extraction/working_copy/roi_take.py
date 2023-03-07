import cv2

# pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Load the image
# filepath = 'D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/CV_Tesseract/Text-Extraction-Table-Image_workOnThis/for_mine_test/AJ.jpg'
filepath = "D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/CV_Tesseract/Text-Extraction-Table-Image_workOnThis/jupyter notess/new.jpg"
image = cv2.imread(filepath)
# image = cv2.resize(img, (650,750), interpolation = cv2.INTER_AREA)
# Display the image and wait for user to select an ROI
r = cv2.selectROI(image)

# Extract the selected ROI
x, y, w, h = r
roi = image[y:y+h, x:x+w]
print(x,y,w,h)
print("extended:", x,y,y+h,x+w)

# Display the extracted ROI
cv2.imshow("ROI", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
