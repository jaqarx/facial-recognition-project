import cv2 as cv
import numpy as np

img = cv.imread("test/cat1234.jpg")
if img is None:
    print("could not find image")
cv.line(img, (0, 0), (100, 100), (255, 0, 0), 5)
pts = np.array([[10, 5], [20, 30], [70, 20], [50, 10]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv.polylines(img, [pts], True, (0, 255, 255))
cv.imshow("Cat", img)
k = cv.waitKey(0)
if k == ord("s"):
    cv.imwrite("test/cat1234.png", img)



#img = np.zeros((500, 600, 3), dtype=np.uint8)
#cv2.line(img, (50, 50), (200, 50), (0, 0, 255), 2)
#cv2.rectangle(img, (250, 100), (400, 200), (0, 255, 0), -1)
#cv2.imshow('Shapes', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows
