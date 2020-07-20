# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import cv2
import imutils
from skimage.filters import threshold_local
#%%
def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	# return the ordered coordinates
	return rect

def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped
#%%
#Function to select 4 points manually on an image
posList=[]
def onMouse(event, x, y, flags, param):
   global posList
   if event == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
        if len(posList) ==4:
            print("4 points selected")
            cv2.destroyAllWindows()

#%%
#Read image and Resize it  
image = cv2.imread("C:/Users/Saurabh/Desktop/walmart bills/bills_images/3.jpeg")
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)
# convert the image to grayscale, blur it, and find edges
# in the image
def edge_detect(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    # show the original image and the edge detected image
    print("STEP 1: Edge Detection")
    cv2.imshow("Image", image)
    cv2.imshow("Edged", edged)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return edged
edged = edge_detect(image)
#%%
def find_and_draw_contours(image,original):
    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts = cv2.findContours(image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    # loop over the contours
    for c in cnts:
    	# approximate the contour
    	peri = cv2.arcLength(c, True)
    	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    	# if our approximated contour has four points, then we
    	# can assume that we have found our screen
    	if len(approx) == 4:
    		screenCnt = approx
    		break
    
    if len(approx)!=4:
        print("4 corner points couldn't be found, please manually select them.")
        cv2.imshow("bill",original)
        cv2.namedWindow('bill')
        cv2.setMouseCallback('bill', onMouse)
        cv2.waitKey(0)
        pos=np.asarray(posList)
        screenCnt = pos.reshape((4,1,2))
        posList.clear()
    im1 =original.copy()    
    im = cv2.drawContours(im1, [screenCnt], -1, (0, 255, 0), 2)
    cv2.imshow("Outline", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return screenCnt
print("STEP 2: Find contours of paper")
# show the contour (outline) of the piece of paper
while True:
    screenCnt = find_and_draw_contours(edged,orig)
    print("Happy with selected contours ? (Y or N)")
    ans = input()
    if ans =='Y':
        break
    
#%%
# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, screenCnt.reshape(4, 2) )
# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset = 10, method = "gaussian")
warped = (warped > T).astype("uint8") * 255
# show the original and scanned images
print("STEP 3: Apply perspective transform")
cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
cv2.waitKey(0)

#%%
