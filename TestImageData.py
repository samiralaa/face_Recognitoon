import cv2 as cv 
import sys 

# Read the image file
img = cv.imread("dddd_face.jpg")
img2 = cv.imread("test_face.jpg")
data = [img,img2]
# Check if the image was successfully loaded
if img is None:
    sys.exit("Could not read the image.")
cv.imshow("Display window", img2)
k = cv.waitKey(0)