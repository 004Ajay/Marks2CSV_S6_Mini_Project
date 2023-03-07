import cv2 as cv

new_filename = 'abdul.jpg'
src = cv.imread(new_filename)
new_src = cv.resize(src, (650,750), interpolation = cv.INTER_AREA)
x, y, w, h = 69, 405, 529, 208
roi_image = new_src[y:y+h, x:x+w]
cv.imshow('roi', roi_image)
cv.waitKey(0)