import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Load the image and convert to grayscale
filepath = "D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/CV_Tesseract/Text-Extraction-Table-Image_workOnThis/images/emil.jpg"
img = cv2.imread(filepath)
image = cv2.resize(img, (650,750), interpolation = cv2.INTER_AREA)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('gray', gray)
# Use edge detection to detect and highlight ROI
edged = cv2.Canny(gray, 50, 200)
# cv2.imshow('edged', edged)

cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Find contours in the image

# Draw a bounding box around the ROI
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if w > 100 and h > 25: # h > 20 will bound name of student in some cases
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

# Crop the image to the bounding box
roi = gray[y:y+h, x:x+w]
cv2.imshow('roi', image)

cv2.waitKey(0)

cv2.destroyAllWindows()   


# # Use pytesseract OCR to extract text
# text = pytesseract.image_to_string(roi)
# print(text)
