import numpy as np
import cv2 as cv
import math
 
drawing = False # true if mouse is pressed
mode = 0 # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1 #initial positions
lastx, lasty = 0, 0 #last x and y positions
img = np.zeros((768, 1024,3), np.uint8)
prevImgs = []

#Finds what x and y directions the mouse is moving in, returning an array of directions
def findDirection(ix, iy, x, y):
    directions = []
    if x > ix:
        directions.append(1)
    elif x == ix:
        directions.append(0)
    else:
        directions.append(-1)
    if y > iy:
        directions.append(1)
    elif y == iy:
        directions.append(0)
    else:
        directions.append(-1)
    return directions

def resetCanvas(img):
    img.fill(0)
    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(img,'(m)ode, (r)eset, (esc)ape, (u)ndo, (s)ave',(10,750), font, 0.8,(255,255,255),2,cv.LINE_AA)

# mouse callback function
# Either draws hollow rectangles or circles depending on mode, which is toggled by pressing "m"
# Circles radius changes depending on mouse move speed
def draw_circle(event, x, y, flags, param):
    global ix,iy,drawing,mode, lastx, lasty, img, prevImgs
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
        lastx, lasty = x, y
    
    elif event == cv.EVENT_MOUSEMOVE:
        rectangleDirection = findDirection(ix, iy, x, y)
        if drawing == True:
            # Detect changed direction
            if mode == 0:
                img = prevImgs[-1].copy()
                a = ix + 5 * rectangleDirection[0]
                b = iy + 5 * rectangleDirection[1]
                c = x - 5 * rectangleDirection[0]
                d = y - 5 * rectangleDirection[1]
                cv.rectangle(img,(ix,iy),(a,y),(0,255,0),-1)
                cv.rectangle(img,(c,iy),(x,y),(0,255,0),-1)
                cv.rectangle(img,(ix,d),(x,y),(0,255,0),-1)
                cv.rectangle(img,(ix,iy),(x,b),(0,255,0),-1)
            elif mode == 1:
                cv.line(img,(lastx, lasty),(x, y),(0,0,255),5)
            elif mode == 2:
                img = prevImgs[-1].copy()
                radius = max(math.sqrt((ix - x) ** 2 + (iy - y) ** 2), 5)
                cv.circle(img, (ix, iy), int(radius), (255, 0, 0), -1)
        lastx, lasty = x, y
    
    elif event == cv.EVENT_LBUTTONUP:
        rectangleDirection = findDirection(ix, iy, x, y)
        drawing = False
        if mode == 0:
            img = prevImgs[-1].copy()
            a = ix + 5 * rectangleDirection[0]
            b = iy + 5 * rectangleDirection[1]
            c = x - 5 * rectangleDirection[0]
            d = y - 5 * rectangleDirection[1]
            cv.rectangle(img,(ix,iy),(a,y),(0,255,0),-1)
            cv.rectangle(img,(c,iy),(x,y),(0,255,0),-1)
            cv.rectangle(img,(ix,d),(x,y),(0,255,0),-1)
            cv.rectangle(img,(ix,iy),(x,b),(0,255,0),-1)
        elif mode == 1:
            cv.line(img,(lastx, lasty),(x, y),(0,0,255),5)
        elif mode == 2:
            radius = max(math.sqrt((ix - x) ** 2 + (iy - y) ** 2), 5)
            cv.circle(img, (ix, iy), int(radius), (255, 0, 0), -1)
        prevImgs.append(img.copy())


resetCanvas(img)
prevImgs.append(img.copy())
cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle)
#cv.namedWindow('prevImg')
 
while(1):
    cv.imshow('image',img)
    #cv.imshow('prevImg', prevImgs[-1])
    k = cv.waitKey(5) & 0xFF
    if k == ord('m'): #Press "m" to toggle mode
        mode += 1
        mode %= 3
    elif k == ord('r'): #Press "r" to reset canvas
        resetCanvas(img)
        prevImgs.append(img.copy())
    elif k == ord('u'): #press "u" to undo
        prevImgs.pop()
        img = prevImgs[-1].copy()
    elif k == ord("s"):
        cv.imwrite("test/cat1234.png", img)
    elif k == 27: #Press esc to escape
        break
 
cv.destroyAllWindows()