import cv2 as cv
import numpy as np

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

def detect_lines(image, title='default', rho = 1, theta = np.pi/180, threshold = 50, minLinLength = 1, maxLineGap = 6, display = False, write = False):
    # Check if image is loaded fine
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    if gray is None:
        print ('Error opening image!')
        return -1
    
    dst = cv.Canny(gray, 50, 150, None, 3)
    
    # Copy edges to the images that will display the results in BGR
    cImage = np.copy(image)
    
    #linesP = cv.HoughLinesP(dst, 1 , np.pi / 180, 50, None, 290, 6)
    linesP = cv.HoughLinesP(dst, rho , theta, threshold, None, minLinLength, maxLineGap)

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
            
    if (display):
        for i, line in enumerate(horizontal_lines):
            cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,255,0), 3, cv.LINE_AA)
            
            cv.putText(cImage, str(i) + "h", (line[0] + 5, line[1]), cv.FONT_HERSHEY_SIMPLEX,  
                       0.5, (0, 0, 0), 1, cv.LINE_AA) 
            
        for i, line in enumerate(vertical_lines):
            cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
            cv.putText(cImage, str(i) + "v", (line[0], line[1] + 5), cv.FONT_HERSHEY_SIMPLEX,  
                       0.5, (0, 0, 0), 1, cv.LINE_AA) 
            
        cv.imshow("Source", cImage) 
        #cv.imshow("Canny", cdstP)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
    if (write):
        cv.imwrite(f"{title}.png", cImage)
        
    return (horizontal_lines, vertical_lines)


new_filename = 'abdul.jpg'
src = cv.imread(new_filename)
new_src = cv.resize(src, (650,750), interpolation = cv.INTER_AREA)
x, y, w, h = 69, 405, 529, 208
roi_image = new_src[y:y+h, x:x+w]
cv.imshow('roi', roi_image)
cv.waitKey(0)


new_horizontal, new_vertical = detect_lines(roi_image, minLinLength=1, display=True, write = True)
# print(new_horizontal,'\n', new_vertical)