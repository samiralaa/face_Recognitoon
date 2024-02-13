import cv2 as cv 
import sys 

# Read the image file
img = cv.imread("ss_face.jpg")

# Check if the image was successfully loaded
if img is None:
    sys.exit("Could not read the image.")
cv.imshow("Open OutPut", img)
k = cv.waitKey(0)
if k == ord("s"):
    cv.imwrite("starry_night.png", img)