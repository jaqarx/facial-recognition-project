import numpy as np
import cv2 as cv
import math
 
drawing = False # true if mouse is pressed
mode = 0 # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1 #initial positions
lastx, lasty = 0, 0 #last x and y positions
img = np.zeros((512, 512,3), np.uint8)
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
    cv.putText(img,'m, r, esc, u, s',(10,500), font, 0.8,(255,255,255),2,cv.LINE_AA)

# mouse callback function
# Either draws hollow rectangles or circles depending on mode, which is toggled by pressing "m"
# Circles radius changes depending on mouse move speed
def draw_rect(x, y):
    rectangleDirection = findDirection(ix, iy, x, y)
    a = ix + 5 * rectangleDirection[0]
    b = iy + 5 * rectangleDirection[1]
    c = x - 5 * rectangleDirection[0]
    d = y - 5 * rectangleDirection[1]
    cv.rectangle(img,(ix,iy),(a,y),(0,255,0),-1)
    cv.rectangle(img,(c,iy),(x,y),(0,255,0),-1)
    cv.rectangle(img,(ix,d),(x,y),(0,255,0),-1)
    cv.rectangle(img,(ix,iy),(x,b),(0,255,0),-1)

def draw_line(x, y):
    cv.line(img,(lastx, lasty),(x, y),(0,0,255),5)

def draw_circle(x, y):
    radius = max(math.sqrt((ix - x) ** 2 + (iy - y) ** 2), 5)
    cv.circle(img, (ix, iy), int(radius), (255, 0, 0), -1)

def checkSame(newPixels, pixel, originalColor, color):
    global img
    if np.all(img[pixel[0], pixel[1]] == originalColor):
        img[pixel[0], pixel[1]] = color
        newPixels.add(pixel)

def draw_fill(x, y, color):
    global img
    originalColor = np.copy(img[y, x])
    img[y, x] = color
    pixels = set()
    originalCoords = (y, x)
    pixels.add(originalCoords)
    i = 0
    while len(pixels) > 0 and i < 100000:
        cv.waitKey(1)
        cv.imshow('image', img)
        newPixels = set()
        for pixel in pixels:
            if (pixel[0] != 0):
                checkSame(newPixels, (pixel[0] - 1, pixel[1]), originalColor, color)
            if (pixel[0] != len(img) - 1):
                checkSame(newPixels, (pixel[0] + 1, pixel[1]), originalColor, color)
            if (pixel[1] != 0):
                checkSame(newPixels, (pixel[0], pixel[1] - 1), originalColor, color)
            if (pixel[1] != len(img[0]) - 1):
                checkSame(newPixels, (pixel[0], pixel[1] + 1), originalColor, color)
        pixels = newPixels
        i += len(pixels)

def on_mouse(event, x, y, flags, param):
    global ix,iy,drawing,mode, lastx, lasty, img, prevImgs
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
        lastx, lasty = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == 0:
                img = prevImgs[-1].copy()
                draw_rect(x, y)
            elif mode == 1:
                draw_line(x, y)
            elif mode == 2:
                img = prevImgs[-1].copy()
                draw_circle(x, y)
        lastx, lasty = x, y
    
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode == 0:
            img = prevImgs[-1].copy()
            draw_rect(x, y)
        elif mode == 1:
            cv.line(img,(lastx, lasty),(x, y),(0,0,255),5)
        elif mode == 2:
            radius = max(math.sqrt((ix - x) ** 2 + (iy - y) ** 2), 5)
            cv.circle(img, (ix, iy), int(radius), (255, 0, 0), -1)
        elif mode == 3:
            color = [255, 255, 255]
            draw_fill(x, y, color)
        prevImgs.append(img.copy())


resetCanvas(img)
prevImgs.append(img.copy())
cv.namedWindow('image')
cv.setMouseCallback('image', on_mouse)
#cv.namedWindow('prevImg')
 
print(img[0, 0])
while(1):
    cv.imshow('image',img)
    #cv.imshow('prevImg', prevImgs[-1])
    k = cv.waitKey(5) & 0xFF
    if k == ord('m'): #Press "m" to toggle mode
        mode += 1
        mode %= 4
    elif k == ord('r'): #Press "r" to reset canvas
        resetCanvas(img)
        prevImgs.append(img.copy())
    elif k == ord('u'): #press "u" to undo
        prevImgs.pop()
        img = prevImgs[-1].copy()
    elif k == ord("s"):
        cv.imwrite("test/drawing.png", img)
    elif k == 27: #Press esc to escape
        break
 
cv.destroyAllWindows()