import numpy as np
import cv2 as cv
import math
 
drawing = False # true if mouse is pressed
mode = 0 # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1 #initial positions
lastx, lasty = 0, 0 #last x and y positions
img = np.zeros((512, 512,3), np.uint8)
settingsImg = np.zeros((200, 450, 3), np.uint8)
rgb = [0, 0, 0]
prevImgs = []

def changeR(position):
    global rgb
    rgb[2] = position

def changeG(position):
    global rgb
    rgb[1] = position

def changeB(position):
    global rgb
    rgb[0] = position

def changeM(position):
    global mode
    mode = position

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
    cv.putText(img,'r, esc, u, s',(10,500), font, 0.8,(255,255,255),2,cv.LINE_AA)

# mouse callback function
# Either draws hollow rectangles or circles depending on mode, which is toggled by pressing "m"
# Circles radius changes depending on mouse move speed
def draw_rect(x, y):
    rectangleDirection = findDirection(ix, iy, x, y)
    a = ix + 5 * rectangleDirection[0]
    b = iy + 5 * rectangleDirection[1]
    c = x - 5 * rectangleDirection[0]
    d = y - 5 * rectangleDirection[1]
    cv.rectangle(img,(ix,iy),(a,y),rgb,-1)
    cv.rectangle(img,(c,iy),(x,y),rgb,-1)
    cv.rectangle(img,(ix,d),(x,y),rgb,-1)
    cv.rectangle(img,(ix,iy),(x,b),rgb,-1)

def draw_line(x, y):
    cv.line(img,(lastx, lasty),(x, y),rgb,5)

def draw_circle(x, y):
    radius = max(math.sqrt((ix - x) ** 2 + (iy - y) ** 2), 5)
    cv.circle(img, (ix, iy), int(radius), rgb, -1)

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
            draw_line(x, y)
        elif mode == 2:
            radius = max(math.sqrt((ix - x) ** 2 + (iy - y) ** 2), 5)
            cv.circle(img, (ix, iy), int(radius), rgb, -1)
        elif mode == 3:
            draw_fill(x, y, rgb)
        prevImgs.append(img.copy())

def draw_settings():
    settingsImg.fill(0)
    if mode == 0:
        cv.rectangle(settingsImg, (125, 10), (325, 190), rgb, 5)
        cv.rectangle(settingsImg, (130, 15), (320, 185), (0, 0, 0), 5)
    elif mode == 1:
        cv.line(settingsImg, (10, 100), (440, 100), rgb, 5)
    elif mode == 2:
        cv.circle(settingsImg, (225, 100), 50, rgb, -1)
    elif mode == 3:
        settingsImg[:] = rgb
resetCanvas(img)
prevImgs.append(img.copy())
cv.namedWindow('image')
cv.setMouseCallback('image', on_mouse)
cv.namedWindow('settings')

cv.createTrackbar('R', 'settings', 255, 255, changeR)
cv.createTrackbar('G', 'settings', 255, 255, changeG)
cv.createTrackbar('B', 'settings', 255, 255, changeB)
cv.createTrackbar('mode', 'settings', 0, 3, changeM)
#cv.namedWindow('prevImg')
 
print(img[0, 0])    
while(1):
    cv.imshow('image',img)
    #cv.imshow('prevImg', prevImgs[-1])
    k = cv.waitKey(5) & 0xFF
    if k == ord('r'): #Press "r" to reset canvas
        resetCanvas(img)
        prevImgs.append(img.copy())
    elif k == ord('u'): #press "u" to undo
        if len(prevImgs) > 1:
            prevImgs.pop()
            img = prevImgs[-1].copy()
    elif k == ord("s"):
        cv.imwrite("test/drawing.png", img)
    elif k == 27: #Press esc to escape
        break
    
    cv.imshow('settings', settingsImg)
    draw_settings()
 
cv.destroyAllWindows()