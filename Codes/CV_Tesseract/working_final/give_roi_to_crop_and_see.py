import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

# Load the image
filepath = "D:/AJAYMON/AJAY/Programming/Auto_Excel_Mark_Entry/Codes/CV_Tesseract/Text-Extraction-Table-Image_workOnThis/images/AJ.jpg"
img = cv2.imread(filepath)
image = cv2.resize(img, (650,750), interpolation = cv2.INTER_AREA)

roi = (69, 413, 529, 208) # ROI coordinates
# rois = [(88, 292, 369, 37),(69, 413, 529, 208)] # ROI coordinates

print(roi)
x, y, w, h = roi
roi_image = image[y:y+h, x:x+w]
cv2.imshow('roi', roi_image)
cv2.waitKey(0)

# Initialize the list to store the extracted text from each ROI
extracted_text = []

# Loop over the ROIs
# for roi in rois:
#     print(roi)
#     x, y, w, h = roi
#     roi_image = image[y:y+h, x:x+w]
#     cv2.imshow('roi', roi_image)
#     cv2.waitKey(0)
#     text = pytesseract.image_to_string(roi_image,  config='digits')
#     extracted_text.append(text)


# print(len(extracted_text))
# for i in extracted_text:
#     print(i)
