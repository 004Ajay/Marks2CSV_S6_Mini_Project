import cv2 as cv
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"


im = cv.imread('a.jpg')

grey = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
# cv.imwrite("gray.png", gray)
thresh = cv.threshold(grey, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1] # breakpoint here ..............................................
# # cv.imshow("bw", bw)
# cv.imwrite("bw.png", bw)
# edged = cv.Canny(thresh, threshold1=127, threshold2=255)
# cv.imwrite("bw_inver.png", bw)
# #bw = erode(bw, kernel_size=2)

print(pytesseract.image_to_string(thresh, config='--psm 6'))

# cv.imshow('original', im)
# cv.imshow('threshold', thresh)
# cv.imshow('edged', edged)
# cv.waitKey(0)
# cv.destroyAllWindows()
